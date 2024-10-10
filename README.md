# NYU Event Sync: Google Calendar Integration with NYU Engage

Our finished web application aims to connect to your Google Calendar and automatically populate it with invitations to events scraped from NYU Engage, based on your personal preferences. Accepting an invite will redirect the user to RSVP for the event. Likewise, rejecting invites will remove the clutter of invites from their Google Calendar space.

## Current Status:

- This is a simple backend application designed to sync Google Calendar events into a MongoDB database. There is no front-end interface — just backend logic for fetching, storing, and updating calendar and student data in the database.
- As a test, we've inserted our own sample data (i.e. name, netid, Google Calender data) to see the functionality of our database and ensure that it's meaningful and representative of real world use.

## Features

- **OAuth (Google) login** for connecting to Google Calendar.
- **Fetch Google Calendar events** and store them in MongoDB.
- **Upsert functionality:** Insert new events or update existing ones in the MongoDB collection.
- **Manual student records can be inserted** for testing purposes.

## Schema and Database Design:

The database uses MongoDB, and the schema includes:
- **Student Bio:** Information such as name, email, netID, and preferences related to event types.
- **Student Calendar:** Calendar entries pulled from Google Calendar linked to a student.
- **Event:** Event details from NYU Engage.
- **Event Calendar:** Tracks the event status for a user, e.g., suggested, accepted, or declined.
Refer to the image ppds_mongodb_schema.jpg for a visual representation of the database schema.


## Prerequisites

- Python 3.11 or higher
- MongoDB Atlas account (or a local MongoDB installation)
- Google API OAuth credentials
- pip (Python package manager)


## Setup

1. Clone this repository or download the source code:
    ```bash
    git clone https://github.com/GiveChoco/PPDS_finalDB.git
    ```

2. Navigate to the project directory:
    ```bash
    cd path/to/your_desired_directory_name_here
    ```

3. Create a virtual environment if you'd like:
    ```bash
    python -m venv .venv
    ```

    - **On Windows:**
        ```bash
        .venv\Scripts\activate
        ```

    - **On macOS and Linux:**
        ```bash
        source .venv/bin/activate
        ```

4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

5. Create a `.env` file in the project root directory with your MongoDB connection string:

    ```bash
    MONGODB_URI=your_mongodb_connection_string_here
    ```

    Replace `your_mongodb_connection_string_here` with your actual MongoDB connection string from Atlas.

## Usage

1. **Main Application** (`main.py`):  
   This is the primary script that:
   - Builds upon the functionality of quickstart.py by adding MongoDB integration, allowing fetched events to be stored, updated, or removed from the database.
   - The main.py file contains all the production-level logic for syncing the Google Calendar with MongoDB.

   Run the main application with:

   ```bash
   python main.py
   ```

2. **Quickstart Script** (`quickstart.py`):  
   A basic script used to:
    - Test the OAuth connection and fetch Google Calendar events initially.
    - It helps you confirm that the connection between the application and the Google Calendar API is functional.

   Run the quickstart script with:

   ```bash
   python quickstart.py
   ```

## Contributers

Group 3:
Jin Lee,
Daniar Zhylangozov,
Nadia Chan,
Ziyue Tao

Contributions to improve the application are welcome. Please feel free to submit a Pull Request.
