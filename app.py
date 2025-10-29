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
    auth_header = request.headers.get("X-Auth-Token", "")

    if auth_header != EXPECTED_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    # získaj JSON payload
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    print("✅ Received:", data)  # zobrazí sa v Render logu

    # tu môžeš uložiť dáta, poslať ďalej, atď.
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
