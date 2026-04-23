# db.py — connects to Atlas and returns the database; called at the top of each route
from pymongo import MongoClient
import os

# Database connection for MongoDB
def get_db():
    client = MongoClient(os.getenv("MONGO_URI"))
    return client["Recipe-Ease"]