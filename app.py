from flask import Flask, request, jsonify

app = Flask(__name__)

# ==========================
# KONFIGURÁCIA
# ==========================
EXPECTED_TOKEN = "jgx500-20205-reset"  # rovnaký ako v EA
# ==========================

@app.route("/", methods=["GET"])
def health_check():
    """Základný test – otvoríš v prehliadači, musí napísať 'OK'."""
    return "OK", 200


@app.route("/ingest", methods=["POST"])
def ingest_data():
    """Prijíma dáta z MT5 EA"""

    # 🔐 Over token
    auth_header = request.headers.get("X-Auth-Token", "")
    if auth_header != EXPECTED_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    # 🧾 Získaj telo požiadavky ako text a skús dekódovať ručne
    try:
        data = request.get_json(force=True)  # 👈 force obíde problém s Content-Type
    except Exception as e:
        print("⚠️ JSON decode error:", e)
        return jsonify({"error": "Invalid JSON format"}), 400

    if not isinstance(data, dict):
        return jsonify({"error": "Malformed payload"}), 400

    # 🔎 Skontroluj potrebné polia
    required = ["symbol", "bid", "ask", "time"]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    # ✅ Vypíš prijaté dáta do logu (Render logy)
    print(f"✅ Received from EA: {data}")

    # môžeš tu pridať ďalšie spracovanie, uloženie, atď.
    return jsonify({"status": "ok", "received": data}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
