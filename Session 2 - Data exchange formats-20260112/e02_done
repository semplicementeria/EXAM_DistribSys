import argparse 
import requests
import yaml  

'''
Objective:
The objective of this exercise is to create a command-line tool that retrieves JSON data 
from a remote source, filters it based on user ID, stores the filtered data locally in YAML format, 
and allows the user to add new TODO items to the local copy.
'''
# 1st Requirement: Configuration of the CLI. Argparse to manage the user's input by the terminal
parser=argparse.ArgumentParser(description="Fetch and filter TODOs")

parser.add_argument( #definition of the URL argument
    "--url",
    type = str,
    default = "https://dummyjson.com/todos", #optional default value
    help = "Remote endpoint URL (default: https://dummyjson.com/todos)"
)

parser.add_argument( #definition of the argument of the user ID. Requested by the text as an integer.
    "--userID",
    type = int,
    default = 1,
    help = "user ID (default 1)"
)

parser.add_argument(#optional argument to specify YAML output file
    "--output",
    type=str,
    default="todos.yaml",
    help="Output YAML file name (default: todos.yaml)"
)

# From here there's the parsing execution: transformation from CLI strings to a Python object
args = parser.parse_args()
print(f"Remote endpoint: {args.url}")
print(f"User ID: {args.userID}")

# 2nd Rquirement: Retrieve remote data: requests module used to interact with web API  
try:
    response = requests.get(args.url, timeout = 10) # GET call to the specified URL with a timeout (just for security reasons)
    response.raise_for_status() # verification to see if al went right (wanted status code: 200)
    data = response.json() # parsing of the JSON responseto transform it in a Python dictionary
    todos=data.get("todos",[]) # we extract the list of the to dos
    print("Data that have been fetched successfully:")
    print(data)
except requests.exceptions.RequestException as e: # here we manage errors (of the network or of the URL as requested in the Additional Notes)
    print(f"No data has been fetched:{e}")
    exit(1)

# 3rd Requirement: Filter data by userID. A new list containig all only the correspondent To Dos to the ID is created.
filtered = [todo for todo in todos if todo.get("userId")==args.userID] 

# 4th Requirement: Print of the filtered user data. Here we have to check if all the to dosare present for all the users before going on
if filtered:
    print(f"TODOs for user {args.userID}")
    for todo in filtered:
        status = "YES" if todo["completed"] else "NO"
        print(f"[{status}] {todo['todo']} (ID: {todo['id']})")
else:
    print(f"Todo not completed by user: {args.userID}")

# 5th Requirement: Save the filtered data locally as a YAML file. We open the file as "w" (writing mode)
with open(args.output, "w") as f:
    yaml.safe_dump(filtered, f, sort_keys=False, indent=2) # with that FALSE we follow the original order 
print(f"Filtered ToDos saved in file {args.output}")

# 6th Requirement: interactive bash for the user in order to append the new info
add_new = input("Do you want to add a new To Do for this user? (Y/N): ").strip().lower() # user-friendly prompt

if add_new == "y":
    new_desc = input("Enter the new To Do description: ").strip() # request for a new to do 

    # generation of a new ID: it finds the max. value among the existing IDs and adds 1
    existing_ids = [todo.get("id", 0) for todo in filtered]
    new_id = max(existing_ids, default = 0) + 1

    # creation of a new todo: new data structure for the new element
    new_todo = {
            "userId": args.userID,
            "id": new_id,
            "todo": new_desc,
            "completed": False
        }

    # append to the local list the new element
    filtered.append(new_todo)

    # update of the local YAML file with new included data:
    with open(args.output, "w") as f:
        yaml.safe_dump(filtered, f, sort_keys=False, indent=2)
    
    print(f"New ToDo added and saved to {args.output}")
