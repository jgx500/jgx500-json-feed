from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# --- tvoj tajný token z EA (musí sa zhodovať s tým v MT5) ---
VALID_TOKEN = "jgx500-20205-reset"

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "JGX500 JSON feed running"}), 200


@app.route("/ingest", methods=["POST"])
def ingest():
    # --- 1️⃣ kontrola tokenu ---
    token = request.headers.get("X-Auth-Token")
    if token != VALID_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    # --- 2️⃣ kontrola typu obsahu ---
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    # --- 3️⃣ dekódovanie JSON ---
    try:
        data = request.get_json(force=True)
    except Exception as e:
        return jsonify({"error": f"JSON decode error: {str(e)}"}), 400

    # --- 4️⃣ validácia kľúčov ---
    required = ["symbol", "bid", "ask", "time"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    # --- 5️⃣ validácia a konverzia času ---
    try:
        ts = datetime.fromisoformat(data["time"])
    except Exception as e:
        return jsonify({"error": f"Invalid time format: {str(e)}"}), 400

    # --- 6️⃣ logovanie prichádzajúcich dát ---
    print(f"[{datetime.now()}] {data['symbol']} @ {ts}: {data['bid']} / {data['ask']}")

    # --- 7️⃣ odpoveď ---
    return jsonify({"status": "ok"}), 200


# --- Flask spustenie ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
