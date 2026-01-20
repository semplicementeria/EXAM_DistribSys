from flask import Flask, request, jsonify #json is a standard used in Python for the communications between server and client. More flexible wrt csv (used in the previous assignment with (worker_id, ts))
#Flask is a lightweight web application framework that allows to quickly setup a web server or web applications in Python
import time, uuid, random #uuid= universally unique identifiers. Different versions, most interesting is the 4th (Random). Adv and Disadv.
import numpy as np

#so we have a server that a user can use to create new random response time generators

app = Flask(__name__) #here we initialize the Flask app:

generators = [] # in order to apply uuid 4 I need a sort of storage of the generators 

#Creation of the source (POST)
@app.route('/response/v1/resources', methods=['POST'])
def create_resource():
   # we have to make sure that the user actually went json:
    if not request.is_json:
        return "request must be JSON\n", 415 #error for the unsupported media type
   
   #we extract the data that has been requested through parsing of the JSON
    data = request.get_json()

    distr = data.get('distr')
    params = data.get('params')
    task = data.get('task')

    if not distr or not params or not task:
      return "Parameters not available", 400 #the resource exists but the input is wrong
   #I'll put the same error for the invalid distribution type and if the task is not in cpu or sleep

    if distr not in ['exponential', 'deterministic', 'uniform']:
      return "Invalid distribution type\n", 400
   
    if task not in ['cpu', 'sleep']: #sleep: it's waiting for something. cpu: there are some computations going on in the processor
      return "Invalid task type\n", 400
    
    #creation of the resource
    resource_id = str(uuid.uuid4())
    new_resource = {
        "id": resource_id,
        "distr": distr,
        "params": params,
        "task": task
    }

    #we create a global list into which we can initialize our generators
    generators.append(new_resource)    
    
    return jsonify(new_resource), 201 #201: request accepted
 
#Then I have to repeat this step but for the GET part:
@app.route('/response/v1/resources', methods=['GET'])
def get_all_resources(): #this function is for all the generators in the list
   return jsonify(generators), 200

@app.route('/response/v1/resources/<string:id>', methods=['GET'])
def get_one_resource(id): #this function is only for one generator if found inside the list that we have generated before.
   for resource in generators:
      if resource["id"] == id:
         return jsonify(resource), 200  #to update the state 
   return "Resource not found\n", 404 #If it is not found
   
#Then I have the PUT part in which we have to update the generator list
@app.route('/response/v1/resources/<string:id>', methods=['PUT'])
def update_resource(id):
    if not request.is_json:
        return "Request must be JSON\n", 415
    data = request.get_json()

    for resource in generators:
        if resource["id"] == id:
            # Update fields if provided
            if "distr" in data:
                if data["distr"] not in ['exponential', 'deterministic', 'uniform']:
                    return "Invalid distribution type\n", 400
                resource["distr"] = data["distr"]
            if "params" in data:
                resource["params"] = data["params"]
            if "task" in data:
                if data["task"] not in ['cpu', 'sleep']:
                    return "Invalid task type\n", 400
                resource["task"] = data["task"]
            return jsonify(resource), 200

    return "Resource not found\n", 404

#From here I implement the DELETE part:
@app.route('/response/v1/resources/<string:id>', methods = ['DELETE'])
def delete_resource(id):
    for r in generators:
        if r["id"] == id:
            generators.remove(r)
            return "", 204
    return "Resource not found", 404

#And then we RUN: 
@app.route('/response/v1/resources/<string:id>/run', methods=['GET'])
def run_resource(id):
    for r in generators:
        if r["id"] == id:
            distr = r["distr"]
            params = r["params"]
            task = r["task"]

            if distr == "deterministic":
                interval = params.get("fixed", 1) #generation of the interval of time
            elif distr == "uniform":
                interval = np.random.uniform(0, params.get("T", 1))
            elif distr == "exponential":
                interval = np.random.exponential(1 / params.get("lambda", 1))
            else:
                return "Invalid distribution\n", 400

            start_time = time.time()

            if task == "sleep":
                # I/O-bound delay (low CPU)
                time.sleep(interval)

            elif task == "cpu":
                # CPU-bound delay (high CPU)
                while time.time() - start_time < interval:
                    x = time.time() - start_time
                    x = float(x) / 3.141592
                    x = float(3.141592) / x

            duration = round(time.time() - start_time, 3)

            return jsonify({
                "id": id,
                "delay": duration,
                "task": task,
                "distr": distr,
                "status": "completed"
            }), 200

    return "Resource not found\n", 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)


#cURL is a command line tool and library for transferring data with URLs to and from servers. 
# It supports many application-layer protocols, including HTTP. Download files, Upload files, Interact with web servers

# TEST: first we have to run the code to run the server in a terminal. In the other...
'''
1) curl -X POST http://localhost:5001/response/v1/resources \
     -H "Content-Type: application/json" \
     -d '{"distr": "deterministic", "params": {"fixed": 3}, "task": "cpu"}' (here we can change the deterministic 
     with the uniform or the exponential by changing the name and the values like...
     
     -d '{"distr": "uniform", "params": {"T": 10}, "task": "sleep"}'
     or:
     -d '{"distr": "exponential", "params": {"lambda": 0.5}, "task": "sleep"}')

2) curl http://localhost:5001/response/v1/resources to see if the server has saved all the resources
and then we run them:
curl http://localhost:5001/response/v1/resources/<ID>/run

3) We can update a resource (for example to a 1-second fixed CPU task):
curl -X PUT http://localhost:5001/response/v1/resources/<ID> \
     -H "Content-Type: application/json" \
     -d '{"distr": "deterministic", "params": {"fixed": 1}, "task": "cpu"}' 

4) and delete it:
curl -X DELETE http://localhost:5001/response/v1/resources/<ID>

5) curl http://localhost:5001/response/v1/resources final check to see if all went right
'''
