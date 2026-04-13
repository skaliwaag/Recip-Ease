from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb+srv://Team:recipe1@recipe-ease.ajuvsog.mongodb.net/recip_ease?retryWrites=true&w=majority")
    return client["recip_ease"]