from dotenv import load_dotenv
import os 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template

# load the environment variables from the .env file
load_dotenv()

# retrieve the MongoDB username and password from the environment variables
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")

# add connection string from MongoDB
# we will need the db_passord from the .env file to complete this connection string
uri = f"mongodb+srv://{username}:{password}@recipe-ease.ajuvsog.mongodb.net/?appName=Recipe-Ease"

# create connection to client
# This will work once we add the cnnection string from mongoDB...
client = MongoClient(uri, server_api=ServerApi('1'))

# ping the server to check the connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Connect to the database
db = client["Recipe-Ease"]

# Connect to users collection
collection = db["users"]


# @app.route("/")
# def home():
#     return render_template("index.html")


