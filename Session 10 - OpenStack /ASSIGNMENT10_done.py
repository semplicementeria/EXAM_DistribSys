import requests
import json

# --- CONFIGURAZIONE DATI ---
# Endpoint richiesto dall'assignment
BASE_URL = "http://10.15.2.1"
AUTH_URL = f"{BASE_URL}:5000/v3/auth/tokens"

# Inserisci qui i tuoi dati reali presi dalla Dashboard
USERNAME = "dist-sys-user1"
PASSWORD = "openstack4DistSys"
PROJECT_ID = "f6af0003bfee4e32ae3ac2107e3a8eaa"

# ID delle risorse (da trovare in Compute -> Images e Compute -> Flavors)
IMAGE_ID = "ee11a82a-1426-44b9-b11b-8b77e0bef276" 
FLAVOR_ID = "2" # Solitamente 1 per m1.small

# --- 1. AUTENTICAZIONE (KEYSTONE) ---
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

print("Richiesta token di autenticazione...")
response = requests.post(AUTH_URL, json=auth_data)

if response.status_code != 201:
    print(f"Errore Auth: {response.text}")
    exit()

token = response.headers['X-Subject-Token']
headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}
print("Token ottenuto con successo.")

# --- 2. CREAZIONE NETWORK (NEUTRON) ---
net_payload = {"network": {"name": "rete_mariapia_auto"}}
res_net = requests.post(f"{BASE_URL}:9696/v2.0/networks", headers=headers, json=net_payload).json()
net_id = res_net['network']['id']
print(f"Network creata con ID: {net_id}")

# --- 3. CREAZIONE SUBNET (NEUTRON) - Necessaria per il boot ---
subnet_payload = {
    "subnet": {
        "name": "subnet_mariapia_auto",
        "network_id": net_id,
        "ip_version": 4,
        "cidr": "192.168.100.0/24",
        "gateway_ip": "192.168.100.1"
    }
}
res_sub = requests.post(f"{BASE_URL}:9696/v2.0/subnets", headers=headers, json=subnet_payload)
if res_sub.status_code == 201:
    print("Subnet creata con successo.")
else:
    print(f"Errore Subnet: {res_sub.text}")
    exit()

# --- 4. CREAZIONE VM (NOVA) ---
# REQUISITO: adminPass deve essere il mio nome
server_payload = {
    "server": {
        "name": "vm_mariapia_auto",
        "imageRef": IMAGE_ID,
        "flavorRef": FLAVOR_ID,
        "adminPass": "Mariapia", 
        "networks": [{"uuid": net_id}],
        "security_groups": [{"name": "default"}]
    }
}

print("Creazione dell'istanza in corso...")
res_server = requests.post(f"{BASE_URL}:8774/v2.1/servers", headers=headers, json=server_payload)

if res_server.status_code == 202:
    print("Successo! L'istanza è stata accettata dal sistema.")
    print(json.dumps(res_server.json(), indent=2))
else:
    print(f"Errore Creazione VM: {res_server.text}")
