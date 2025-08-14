# app.py
from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from db import get_latest_metrics

load_dotenv()  # ensure MONGODB_URI is loaded

app = Flask(__name__)

@app.route("/metrics/<symbol>", methods=["GET"])
def metrics(symbol):
    """
    GET /metrics/BTC  → returns JSON like:
    {
      "symbol": "BTC",
      "name": "Bitcoin",
      "pct_change_30d": 10.12,
      "pct_change_90d": 24.78,
      "volatility_score": -54.96,
      "computed_at": "2025-07-25T00:00:00Z"
    }
    """
    symbol = symbol.upper()
    doc = get_latest_metrics(symbol)
    if not doc:
        return jsonify({"error": f"No metrics found for {symbol}"}), 404

    # clean up BSON types
    response = {
        "symbol":           doc["symbol"],
        "name":             doc["name"],
        "pct_change_30d":   doc.get("30dChange(%)"),
        "pct_change_90d":   doc.get("90dChange(%)"),
        "volatility_score": doc.get("volatility_score"),
        "computed_at":      doc["computed_at"].isoformat()
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
