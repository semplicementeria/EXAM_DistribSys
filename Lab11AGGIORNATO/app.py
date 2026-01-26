from flask import Flask, jsonify
import json
import os
import uuid

app = Flask(__name__)

# The exact directory path from the text of the assignment
CONFIG_PATH = "/etc/my_res.json"

# Global list to store the resources loaded at boot
generators = []

def load_boot_resources():
    """
    Reads the JSON file at /etc/my_res.json.
    Maps 'name' and 'value' from the ConfigMap into my internal list.
    """
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                boot_data = json.load(f)
                
                if isinstance(boot_data, list):
                    for res in boot_data:
                        # Constructing the resource object using the JSON keys
                        resource = {
                            "id": str(uuid.uuid4()),  # Generates a unique ID for internal use
                            "name": res.get("name", "Unknown"),
                            "value": res.get("value", "No Value Provided"),
                            "params": {"fixed": 1} # Default wait time
                        }
                        generators.append(resource)
                    print(f"[*] Successfully loaded {len(generators)} resources.", flush=True)
                else:
                    print("[!] Error: JSON at /etc/my_res.json is not a list.", flush=True)
        except Exception as e:
            print(f"[!] Error reading config file: {e}", flush=True)
    else:
        print(f"[!] File {CONFIG_PATH} not found. Ensure ConfigMap is mounted.", flush=True)

# Load the Alpha and Beta resources before starting the server
load_boot_resources()

@app.route("/")
def welcome():
    return "<h1>REST Server: Alpha & Beta Resources Loaded</h1>\n"

@app.route('/response/v1/resources', methods=['GET'])
def get_all_resources():
    """Returns everything loaded from the ConfigMap."""
    return jsonify(generators), 200

@app.route('/response/v1/generate/<resource_name>', methods=['GET'])
def get_resource_by_name(resource_name):
    """
    Allows to query a resource by name (e.g., /resource1).
    """
    # Find the resource where 'name' matches the URL parameter
    res = next((g for g in generators if g["name"] == resource_name), None)
    
    if not res:
        return jsonify({
            "error": "Resource not found", 
            "requested": resource_name,
            "available": [g["name"] for g in generators]
        }), 404
    
    return jsonify({
        "status": "success",
        "resource_name": res["name"],
        "resource_value": res["value"]
    })

if __name__ == "__main__":
    # Standard port 5000 as defined in the Service targetPort
    app.run(host="0.0.0.0", port=5000)

