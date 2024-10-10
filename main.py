import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
import datetime
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
events = db.get_collection('events')
event_cal = db.get_collection('events_calendar')

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


def add_events(obj):
    """
    Inserts an event into the 'events' collection in MongoDB.
    
    Args:
    obj (dict): A dictionary representing the event with keys:
        - name (str): Event title
        - description (str): Event description
        - category (str): Event category (e.g. STEM, arts)
        - venue (str): Event location
        - startTime (datetime): Event start time
        - endTime (datetime): Event end time
        - createdAt (datetime): When the event was scraped
        - source (str): Source of the event (e.g. 'NYU Engage')
    
    Returns:
    The inserted document's ID.
    """
    # Ensure required fields are present
    required_fields = ['name', 'description', 'category', 'venue', 'startTime', 'endTime', 'createdAt', 'source']
    
    # Check for missing fields
    for field in required_fields:
        if field not in obj:
            raise ValueError(f"Missing required field: {field}")
    
    # Insert the document into the collection
    result = events.insert_one(obj)
    
    # Return the inserted ID
    return result.inserted_id


def create_event_calendar(user_id, event_id, status="suggested"):
    """
    Creates a new event calendar record for the user with the suggested event.

    Args:
    user_id (ObjectId): The ID of the user to whom the event is being suggested.
    event_id (ObjectId): The ID of the event being suggested.
    status (str): The status of the event suggestion, e.g., "suggested", "accepted", "declined".
                  Defaults to "suggested".

    Returns:
    ObjectId: The inserted document's ID.
    """
    # Construct the event dictionary
    event_obj = {
        "eventId": ObjectId(event_id),
        "suggestedAt": datetime.utcnow(),
        "status": status,
        "addedToCalendarAt": None if status == "suggested" else datetime.utcnow()
    }

    # Create the event calendar entry for the user
    calendar_entry = {
        "_id": ObjectId(),  # MongoDB will generate this automatically if you want
        "userId": ObjectId(user_id),
        "events": [event_obj]
    }

    # Insert the new document into the 'events_calendar' collection
    result = event_cal.insert_one(calendar_entry)
    
    # Return the ID of the inserted document
    return result.inserted_id


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
  

   dummy_event_data = {
    "_id": ObjectId(),  # Let MongoDB generate this automatically if desired
    "name": "STEM Workshop: AI in Healthcare",
    "description": "An interactive workshop exploring AI applications in healthcare.",
    "category": "STEM",
    "venue": "NYU Abu Dhabi, Room A301",
    "startTime": datetime(2024, 10, 20, 10, 30),  # Example start time: Oct 20, 2024, 10:30 AM
    "endTime": datetime(2024, 10, 20, 12, 0),  # Example end time: Oct 20, 2024, 12:00 PM
    "createdAt": datetime.utcnow(),  # The current time when it was scraped/created
    "source": "NYU Engage"
    }

# Call the add_events function with the dummy data
   event_id = add_events(dummy_event_data)
   dummy_user_id = ObjectId()  # Example user ID 

   create_event_calendar(
    user_id= dummy_user_id,
    event_id= event_id,
    status="suggested"  # Status can be "suggested", "accepted", or "declined"
    )

if __name__ == "__main__":
    main()