from flask import Flask, request, jsonify
import os, time

app = Flask(__name__)

# Token čítaný výhradne z prostredia Render – bez fallback hodnoty
AUTH_TOKEN = os.environ["AUTH_TOKEN"]
print(f"[DEBUG] Loaded AUTH_TOKEN from env: {AUTH_TOKEN}")

@app.route("/healthz", methods=["GET"])
def healthz():
    return jsonify({"ok": True, "time": time.time()})

@app.route("/ingest", methods=["POST"])
def ingest():
    auth_header = request.headers.get("Authorization", "")
    token = ""
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
    elif auth_header:
        token = auth_header
    else:
        token = request.headers.get("X-Auth-Token", "")

    if token.strip() != AUTH_TOKEN.strip():
        return jsonify({"error": "unauthorized", "received": token}), 401

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "no data"}), 400

    print(f"[FEED] {data}")
    return jsonify({"ok": True, "received": data}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
