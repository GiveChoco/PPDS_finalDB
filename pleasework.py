from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv


mongodb_uri = "mongodb+srv://test1:HDfeAFkJ7ydMja@ppds.kg0g4.mongodb.net/?retryWrites=true&w=majority&appName=PPDS"

# Create a new client and connect to the server
client = MongoClient(mongodb_uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)