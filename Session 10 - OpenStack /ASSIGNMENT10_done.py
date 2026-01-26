import requests
import json

#Configuration Part:
#Here I specify the requested endpoint
BASE_URL = "http://10.15.2.1"
AUTH_URL = f"{BASE_URL}:5000/v3/auth/tokens"

#The following are the data takn from the dashboard
USERNAME = "dist-sys-user1"
PASSWORD = "openstack4DistSys"
PROJECT_ID = "f6af0003bfee4e32ae3ac2107e3a8eaa"

#Resource identifications (taken from Compute>Instances, I clicked on mine and see all the identifications
IMAGE_ID = "ee11a82a-1426-44b9-b11b-8b77e0bef276" 
FLAVOR_ID = "2" 

#Authentication Part:
auth_data = {
    "auth": {
        "identity": {
            "methods": ["password"],
            "password": {
                "user": {
                    "name": USERNAME,
                    "domain": {"id": "default"},
                    "password": PASSWORD
                }
            }
        },
        "scope": {
            "project": {"id": PROJECT_ID}
        }
    }
}

print("Authentication token requested...")
response = requests.post(AUTH_URL, json=auth_data)

if response.status_code != 201:
    print(f"Authentication error: {response.text}")
    exit()

token = response.headers['X-Subject-Token']
headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}
print("Success in the authentication")

#Network creation Part:
net_payload = {"network": {"name": "mariapiaNet"}}
res_net = requests.post(f"{BASE_URL}:9696/v2.0/networks", headers=headers, json=net_payload).json()
net_id = res_net['network']['id']
print(f"Network created with the ID: {net_id}")

#Subnet creation:
subnet_payload = {
    "subnet": {
        "name": "mariapiaSubnet",
        "network_id": net_id,
        "ip_version": 4,
        "cidr": "192.168.100.0/24",
        "gateway_ip": "192.168.100.1"
    }
}
res_sub = requests.post(f"{BASE_URL}:9696/v2.0/subnets", headers=headers, json=subnet_payload)
if res_sub.status_code == 201:
    print("Subnet has been created")
else:
    print(f"Subnet error: {res_sub.text}")
    exit()

#VM creation
server_payload = {
    "server": {
        "name": "mariapiaVM",
        "imageRef": IMAGE_ID,
        "flavorRef": FLAVOR_ID,
        "adminPass": "Mariapia", 
        "networks": [{"uuid": net_id}],
        "security_groups": [{"name": "default"}] 
   }
}

print("Creating the instance...")
res_server = requests.post(f"{BASE_URL}:8774/v2.1/servers", headers=headers, json=server_payload)

if res_server.status_code == 202:
    print("Instance has been created!")
    print(json.dumps(res_server.json(), indent=2))
else:
    print(f"Error in creating VM: {res_server.text}")
