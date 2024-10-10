import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from quickstart import fetch_google_calendar_events
import json
from datetime import datetime

load_dotenv()
mongodb_uri = mongodb_uri = os.getenv('MONGODB_URI')
#from professor's set up 

client = MongoClient(mongodb_uri) # this creates a client that can connect to our DB
print("Databases available:")
print(client.list_database_names()) # just to make sure you are connecting to the right server...
db = client.get_database("Students") # this gets the database named 'Students'
students = db.get_collection("student bio") 
    
client.server_info() # this is a hack to force the client to connect to the server so we can error out
print("Connected successfully to the student bio database")

def add_student_record(email, event_types, availability, calendar_id):

    student = {
    "_id": ObjectId(),  #Unique user ID
    "email": email,  #User's email for Google login
    #"oauthToken": {
    #json file reference 
    #},
  "preferences": {
    "eventTypes": event_types, #array of Preferred event types (e.g. STEM, sports)
    "availability": [
      {
          #will fix to have more accuracy & connection with google calendar
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

def update_student_calendarId(user_id, calendar_id):
    myquery = { "_id": user_id }
    newvalues = { "$set": { "calendarId": calendar_id } }

    students.update_one(myquery, newvalues)


def add_student_calendar(event, user_id,json_filepath):
    student_db = client.get_database("Students")
    calendar = student_db.get_collection("student calendar") 

    #fetch event data 
    source_data = {
            'id': event['id'],
            'title': event.get('summary', 'No Title'),
            'description': event.get('description','No description'),
            'start': event['start'].get('dateTime', event['start'].get('date')),
            'end': event['end'].get('dateTime', event['end'].get('date')),
            'location':event.get('location','No location'),
            'status':event.get('status','No Status'),
        }
    
    with open(json_filepath, 'r') as file:
        data = json.load(file)  # Load the JSON data into a Python dictionary
        expiry = data.get("expiry", "No expiry found")  # Access "expiry" key
        expiry_date = datetime.strptime(expiry, '%Y-%m-%dT%H:%M:%S.%fZ')
        input_expiry = expiry_date.strftime("%B %d, %Y, %I:%M %p")

    event_data = {
     "_id": ObjectId(),  #Unique calendar ID
    "userId": user_id,  #Reference to the user
    "events": [
    {
      "eventId": source_data['id'],  #Event ID from Google Calendar
      "title": source_data['title'],  #Event title
      "description": source_data['description'],  #Event description
      "startTime": source_data['start'],  #Event start time
      "endTime": source_data['end'],  #Event end time
      "location": source_data['location'],  #Event location
      "status": source_data['status'],  #e.g., "confirmed", "cancelled"
      #"source": String  // "Google" or "NYU Engage"
    }
    ],

    "calendar_API expiry (last accessed date)": input_expiry
    }

    calendar.update_one({'id': event_data['_id']}, {'$set': event_data}, upsert=True)

def main():
    events = fetch_google_calendar_events()
    add_student_record('jl13844@nyu.edu',['STEM',"Entrepreneurship","Networking"],['M','12:30 PM','5 PM'],ObjectId())
    add_student_calendar(events[1],students.find_one( {'email' : 'jl13844@nyu.edu'}, {'_id': 1}),'/Users/jinlee/Desktop/PPDS_week4/token.json')
    print("insertion successful")


    student_calendar = db.get_collection("student calendar") 
    student = students.find_one( {'email' : 'jl13844@nyu.edu'}, {'_id': 1})
    student_id = student['_id']
    print(student_id)
    update_student_calendarId(student_id,student_calendar.find_one({'userId._id': student_id},{'_id': 1}))
    print("update successful")
   

if __name__ == "__main__":
    main()