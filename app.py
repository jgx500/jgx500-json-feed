from flask import Flask, request, jsonify
import os, time

app = Flask(__name__)

# token – nechaj ten, čo používaš v EA
AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "jgx500-secure-token")

# tvoje reálne symboly (možno rozšíriť kedykoľvek)
ALLOWED_SYMBOLS = {"SP500", "SP500ft", "BTCUSD", "XAUUSD+"}

# posledný prijatý balík
FEED_DATA = {}

@app.get("/healthz")
def healthz():
    return jsonify(ok=True, ts=int(time.time()))

@app.post("/ingest")
def ingest():
    # jednoduché overenie tokenu
    if request.headers.get("X-Auth-Token") != AUTH_TOKEN:
        return jsonify(error="unauthorized"), 401

    data = request.get_json(silent=True) or {}
    symbol = data.get("symbol")
    bid    = data.get("bid")
    ask    = data.get("ask")

    # očakávame presne {symbol,bid,ask}
    if symbol is None or bid is None or ask is None:
        return jsonify(error="invalid format: need {symbol,bid,ask}"), 400

    # ⬇️ ak chceš striktne kontrolovať symboly, nechaj if; ak chceš prijímať hocijaké názvy, vyhoď tento blok
    if symbol not in ALLOWED_SYMBOLS:
        # namiesto odmietnutia môžeme aj akceptovať – potom stačí return jsonify(ok=True)
        # return jsonify(error=f"unknown symbol: {symbol}"), 400
        pass

    FEED_DATA.update({
        "symbol": symbol,
        "bid": bid,
        "ask": ask,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    })
    return jsonify(ok=True)

@app.get("/feed.json")
def feed():
    if not FEED_DATA:
        return jsonify(error="no data yet"), 404
    return jsonify(FEED_DATA)

if __name__ == "__main__":
    # dôležité kvôli Renderu – používa dynamický PORT
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
