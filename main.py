import os
from dotenv import load_dotenv
import pymongo
from bson.objectid import ObjectId
import datetime
#from pymongo import MongoClientd
from quickstart import fetch_google_calendar_events

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
events = db.get_collection('events')
event_cal = db.get_collection('events_calendar')

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

def save_events_to_mongo(events):
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
   #add_student_record()
   #will_this_work()
#    events = fetch_google_calendar_events()
#    save_events_to_mongo(events)

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