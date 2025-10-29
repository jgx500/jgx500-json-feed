from flask import Flask, request, jsonify
import os
import time

app = Flask(__name__)

# Token – ak nie je v prostredí, nastav default
AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "jgx500-secure-token")

# Zdravotná kontrola
@app.route("/healthz", methods=["GET"])
def healthz():
    return jsonify({"ok": True, "time": time.time()})

# Príjem dát z MT5
@app.route("/ingest", methods=["POST"])
def ingest():
    auth_header = request.headers.get("Authorization", "")
    token = ""

    # Povolené formáty hlavičiek
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
    elif auth_header:
        token = auth_header
    else:
        token = request.headers.get("X-Auth-Token", "")

    # Overenie tokenu
    if token != AUTH_TOKEN:
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "no data"}), 400

    print(f"[FEED] {data}")
    return jsonify({"ok": True, "received": data}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
