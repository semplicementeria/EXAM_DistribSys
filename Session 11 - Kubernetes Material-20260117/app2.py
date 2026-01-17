from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Percorso richiesto dall'esercizio
CONFIG_PATH = "/etc/my_res.json"

def load_resources():
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e), "msg": "Assicurati che il ConfigMap sia montato correttamente"}

# Caricamento al boot
data_at_boot = load_resources()

@app.route('/')
def index():
    return jsonify({
        "status": "Server running",
        "resources": data_at_boot
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
