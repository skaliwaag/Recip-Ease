from pymongo import MongoClient
import os

# Database connection for MongoDB
def get_db():
    client = MongoClient(os.getenv("MONGO_URI"))
    return client["Recipe-Ease"]