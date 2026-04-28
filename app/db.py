# db.py — connects to Atlas and returns the database; called at the top of each route
from pymongo import MongoClient
import os

# New MongoClient per call is intentional for simplicity — a production app would reuse
# a module-level client so the internal connection pool is shared across requests.
def get_db():
    client = MongoClient(os.getenv("MONGO_URI"))
    return client["Recipe-Ease"]