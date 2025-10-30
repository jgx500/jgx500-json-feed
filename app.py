from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# ======================================================
# ✅ ROUTE: /ingest  – prijíma JSON z MT5 (JGX500 EA)
# ======================================================
@app.route("/ingest", methods=["POST"])
def ingest():
    # --- DEBUG výpisy, aby sme videli, čo reálne dorazí ---
    print("-------------------------------------------------")
    print("HEADERS:", dict(request.headers))
    print("RAW BODY:", request.data)

    # --- Pokus o dekódovanie JSON ---
    try:
        # force=True = prečíta JSON aj keď chýba Content-Type
        data = request.get_json(force=True)
        print("PARSED JSON:", data)
    except Exception as e:
        print("❌ JSON decode error:", str(e))
        return jsonify({"error": f"JSON decode error: {str(e)}"}), 400

    # --- Kontrola, či JSON obsahuje základné polia ---
    required_keys = ["symbol", "bid", "ask", "time"]
    missing = [k for k in required_keys if k not in data]
    if missing:
        print("❌ Missing fields:", missing)
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    # --- Parsovanie času (ISO alebo s medzerou) ---
    ts_raw = str(data["time"])
    try:
        ts = datetime.fromisoformat(ts_raw)
    except Exception:
        try:
            ts = datetime.strptime(ts_raw, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print("❌ Time parse error:", e)
            return jsonify({"error": f"Bad time format: {ts_raw}"}), 400

    # --- Výpis prijatých dát na serveri ---
    print(f"✅ Received from EA → {data['symbol']} @ {ts} | bid:{data['bid']} ask:{data['ask']}")

    # --- Odpoveď späť do MT5 ---
    return jsonify({"status": "ok", "symbol": data["symbol"], "time": ts_raw}), 200


# ======================================================
# ✅ Základná testovacia route (GET /)
# ======================================================
@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "service": "JGX500 JSON Feed",
        "status": "running",
        "usage": "POST JSON data to /ingest"
    }), 200


# ======================================================
# ✅ Spustenie servera
# ======================================================
if __name__ == "__main__":
    # Render beží v prostredí, kde port = 10000
    app.run(host="0.0.0.0", port=10000)
