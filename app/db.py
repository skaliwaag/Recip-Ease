# db.py — connects to Atlas and returns the database; called at the top of each route
from pymongo import MongoClient
import os

# new client every call is fine for a class project, but a real app would reuse
# one client so the connection pool is shared instead of rebuilt each time
def get_db():
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise RuntimeError(
            "MONGO_URI is not set. Copy .env.example to .env and fill in your Atlas connection string."
        )
    client = MongoClient(uri)
    return client["Recipe-Ease"]
