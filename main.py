from dotenv import load_dotenv  
# ***** need to make ".env" file for password stuff for our database, and make sure to hide it on windows*****
import os 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# load the environment variables from the .env file
load_dotenv()
# retrieve the MongoDB username and password from the environment variables
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")

# add connection string from MongoDB
# we will need the db_passord from the .env file to complete this connection string
uri = "mongodb+srv://<db_username>:<db_password>@recipe-ease.ajuvsog.mongodb.net/?appName=Recipe-Ease"

# create connection to client
# This will work once we add the cnnection string from mongoDB...
client = MongoClient(uri, server_api=ServerApi('1'))

# ping the server to check the connection
client.admin.command ('ping')
print("We are connected!")

# Connect to the database
db = client["Recipe-Ease"]