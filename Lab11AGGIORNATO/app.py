from flask import Flask, request, jsonify
import time, uuid, random, json, os
import numpy as np

app = Flask(__name__)

# Percorso del file montato dalla ConfigMap
CONFIG_PATH = "/etc/my_res.json"

# Archivio globale per i generatori
generators = []

def load_boot_resources():
    """Carica le risorse dal file JSON all'avvio e le adatta al formato interno."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                boot_data = json.load(f)
                
                # Se il JSON è una lista, lo processiamo
                if isinstance(boot_data, list):
                    for res in boot_data:
                        # Assicuriamoci che ogni risorsa abbia i campi necessari per funzionare
                        # Se mancano (come nel tuo caso 'name'/'value'), mettiamo dei default
                        resource = {
                            "id": res.get("id", str(uuid.uuid4())),
                            "distr": res.get("distr", "deterministic"),
                            "params": res.get("params", {"fixed": 1}),
                            "task": res.get("task", "sleep"),
                            "name_metadata": res.get("name", "Legacy Resource"),
                            "value_metadata": res.get("value", "No value")
                        }
                        generators.append(resource)
                    print(f"[*] Caricate {len(generators)} risorse da {CONFIG_PATH}", flush=True)
                else:
                    print("[!] Errore: Il file JSON deve contenere una lista.", flush=True)
        except Exception as e:
            print(f"[!] Errore durante la lettura del file JSON: {e}", flush=True)
    else:
        print(f"[!] File {CONFIG_PATH} non trovato. Partenza con lista vuota.", flush=True)

# Eseguiamo il caricamento prima che il server inizi a rispondere
load_boot_resources()

@app.route("/")
def welcome():
    return "<h1>The random response time server is running!</h1>\n"

@app.route('/response/v1/resources', methods=['GET'])
def get_all_resources():

