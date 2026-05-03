# Connects to MongoDB Atlas and returns the database object.
# Every route that needs to read or write data calls get_db() at the top.
from pymongo import MongoClient
import os

# A new MongoClient is created on every call, which means a fresh TCP connection
# each time. For a class project hitting a small Atlas cluster this is fine.
# A production app would hold one shared client so pymongo can manage its own
# connection pool across requests.
def get_db():
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise RuntimeError(
            "MONGO_URI is not set. Copy .env.example to .env and fill in your Atlas connection string."
        )
    client = MongoClient(uri)
    return client["Recipe-Ease"]
