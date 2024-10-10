import os
from dotenv import load_dotenv
import pymongo
from bson.objectid import ObjectId
#from pymongo import MongoClientd
from pymongo.mongo_client import MongoClient
from quickstart import fetch_google_calendar_events

load_dotenv()
mongodb_uri = os.getenv('MONGODB_URI')



#from professor's set up 

client = pymongo.MongoClient(mongodb_uri) # this creates a client that can connect to our DB
print("Databases available:")
print(client.list_database_names()) # just to make sure you are connecting to the right server...
db = client.get_database("Students") # this gets the database named 'Students'
students = db.get_collection("student bio") 
    
client.server_info() # this is a hack to force the client to connect to the server so we can error out
print("Connected successfully to the student bio database")

#C of CRUD - create 
def add_student_record(email, event_types, availability, calendar_id):

    student = {
    "_id": ObjectId(),  #Unique user ID
    "email": email,  #User's email for Google login
    "oauthToken": {
    #json file reference 
  },
  "preferences": {
    "eventTypes": event_types, #array of Preferred event types (e.g. STEM, sports)
    "availability": [
      {
          #availability - array of user's information
        "day": availability[0],  # Day of the week
        "startTime": availability[1],  #Start of available window
        "endTime": availability[2]  #End of available window
      }
    ]
  },
  "calendarId": calendar_id #Reference to the user's Google Calendar data
    }
    
    result = students.insert_one(student)
    print(f"User inserted with ID: {result.inserted_id}")



def add_student_calendar(events):
    student_db = client.get_database("Students")
    calendar = student_db.get_collection("student calendar") 
    for event in events:
        event_data = {
            'id': event['id'],
            'summary': event.get('summary', 'No Title'),
            'start': event['start'].get('dateTime', event['start'].get('date')),
            'end': event['end'].get('dateTime', event['end'].get('date'))
        }
        # Upsert (insert if not exists, update if exists)
        calendar.update_one({'id': event['id']}, {'$set': event_data}, upsert=True)

def main():
   #add_student_record()
   #will_this_work()
   events = fetch_google_calendar_events()
   save_events_to_mongo(events)

if __name__ == "__main__":
    main()