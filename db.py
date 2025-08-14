# db.py
import os
from pymongo import MongoClient, ReplaceOne
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId

load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client.get_default_database()
collection = db.loan_agent_metrics

def upsert_metric(doc: dict):
    """
    Upsert a single metric doc by symbol + computed_at date.
    """
    filter_ = {"symbol": doc["symbol"]}
    # Replace or insert
    return collection.replace_one(filter_, doc, upsert=True)

def get_latest_volatility(symbol: str) -> float | None:
    """
    Returns the most recent volatility_score for `symbol`,
    or None if no document is found.
    """
    doc = (
        collection
        .find({"symbol": symbol})
        .sort("computed_at", -1)
        .limit(1)
        .try_next()  # PyMongo ≥ 4.0; use .next() in older versions
    )
    return doc.get("volatility_score") if doc else None


def get_latest_metrics(symbol: str) -> dict | None:
    """
    Returns the most recent document for `symbol`, or None if not found.
    """
    doc = (
        collection
        .find({"symbol": symbol})
        .sort("computed_at", -1)
        .limit(1)
        .next()
    )
    return doc