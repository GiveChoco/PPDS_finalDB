import os
from dotenv import load_dotenv
import pymongo
from bson.objectid import ObjectId
#from pymongo import MongoClientd

load_dotenv()
mongodb_uri = os.getenv('MONGODB_URI')

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


#from professor's set up 

client = pymongo.MongoClient(mongodb_uri) # this creates a client that can connect to our DB
print("Databases available:")
print(client.list_database_names()) # just to make sure you are connecting to the right server...
db = client.get_database("Students") # this gets the database named 'campy'
students = db.get_collection("student bio") 
    
client.server_info() # this is a hack to force the client to connect to the server so we can error out
print("Connected successfully to the student bio database")

def add_student_record():
    name = input("You name: ")
    netid = input("your netid: ")

    student = {
        "name":name,
        "netid":netid
    }

    result = students.insert_one(student)

def will_this_work():
    name = "jin Lee"
    netid ='jl13844'
    sleep_time = "10:44 AM"
    sleep_duration = 5

    student = {
        "name":name,
        "netid":netid,
        "sleep_time":sleep_time,
        "sleep_duration": sleep_duration
    }

    result = students.insert_one(student)

def main():
   add_student_record()
   will_this_work()

if __name__ == "__main__":
    main()