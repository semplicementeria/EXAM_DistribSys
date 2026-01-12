'''Write the python code to run a Flask server exposing a REST API that allows the creation/modification/deletion 
of resources offered by a "random response time" web application. Each resource must represent a generator of response times following a given random distribution, 
with specified parameter(s), mimicking the diverse computation time of some web application server'''

from flask import Flask, request, jsonify
import time, uuid, random
import numpy as np

#so we have a server that a user can use to create new random response time generators
#here we initialize the Flask app:
app = Flask(__name__)

# I create a global storage for the generators
generators = []

#Creation of the source (POST)
@app.route('/response/v1/resources', methods=['POST'])
def create_resource():
   # we have to make sure that the user actually went json:
    if not request.is_json:
        return "request must be JSON\n", 415 #error for the unsupported media type
   
   #now that we know it's JSON then we extract the data that has been requested: parsing of the JSON
    data = request.get_json()

   #then we extract the data and validate the fields that are our parameters we're interested into
    distr = data.get('distr')
    params = data.get('params')
    task = data.get('task')

   #now here i put some other errors
    if not distr or not params or not task:
      return "Parameters not available", 400 #the resource exists but the input is wrong
   #I'll put the same error for the invalid distribution type and if the task is not in cpu or sleep

    if distr not in ['exponential', 'deterministic', 'uniform']:
      return "Invalid distribution type\n", 400
   
    if task not in ['cpu', 'sleep']:
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

    #every resource has to allocate memory in it so I have to create the following structure:
    
    
    #now I have to store them in a global list and append my new objects:
    return jsonify(new_resource), 201
 
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

            # --- Generate random delay ---
            if distr == "deterministic":
                interval = params.get("fixed", 1)
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

#tests for the app.rout:
@app.route("/")
def welcome():
    return "<h1>The random response time server is running!</h1>\n"

@app.route("/test/")
def test():
    return "<h1>This is the test folder.</h1>\n"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)


# TEST:
'''
Create a new resource: curl -X POST http://localhost:5001/response/v1/resources  -H "Content-Type: application/json" -d '{"distr": "deterministic", "params": {"fixed": 2}, "task": "sleep"}'
To see all resources: curl http://localhost:5001/response/v1/resources
To run the resources ( so to simulate the delay): curl http://localhost:5001/response/v1/resources/3a4d6d2a-8c8f-4a2c-ae9e-6ad6d9b5f2c1/run
To update the resources: curl -X PUT http://localhost:5001/response/v1/resources/3a4d6d2a-8c8f-4a2c-ae9e-6ad6d9b5f2c1 -H "Content-Type: application/json" -d '{"distr": "exponential", "params": {"lambda": 0.5}, "task": "cpu"}'
To delete the resources: curl -X DELETE http://localhost:5001/response/v1/resources/3a4d6d2a-8c8f-4a2c-ae9e-6ad6d9b5f2c1
Then we can check the list again: curl http://localhost:5001/response/v1/resources
'''
