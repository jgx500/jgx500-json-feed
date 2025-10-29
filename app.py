from flask import Flask, request, jsonify, send_file
import os, json, time

app = Flask(__name__)
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "jgx500-secure-token")
FEED_PATH = "feed.json"

@app.get("/healthz")
def healthz():
    return {"ok": True, "ts": int(time.time())}

@app.get("/feed.json")
def feed():
    if not os.path.exists(FEED_PATH):
        return jsonify({"error": "no data yet"}), 404
    return send_file(FEED_PATH, mimetype="application/json")

@app.post("/ingest")
def ingest():
    token = request.headers.get("X-Auth-Token", "")
    if token != AUTH_TOKEN:
        return jsonify({"error": "unauthorized"}), 401

    payload = request.get_json(force=True)
    with open(FEED_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    return jsonify({"ok": True, "stored": payload})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

