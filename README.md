# NYU Event Sync: Google Calendar Integration with NYU Engage

- Our finished web application will (hopefully) connect to your Google Calendar and automatically populate it with *invitations* to events scraped from NYU Engage based on your personal preferences. Accepting an invite would redirect the user to go ahead and RSVP for the event. Likewise rejecting invites would remove the clutter of invites from their Google Calender space.
- But for now, this is a simple backend application designed to sync Google Calendar events into a MongoDB database. There's no front-end interface — just backend logic for fetching, storing, and updating calendar and student data in the database.
- As a test, we've inserted our own sample data (i.e. name, netid, sleep time, Google Calender data) to see the functionality of our database and ensure that it's meaningful and representative of real world use.

## Features

- **OAuth (Google) login** for connecting to Google Calendar.
- **Fetch Google Calendar events** and store them in MongoDB.
- **Upsert functionality:** Insert new events or update existing ones in the MongoDB collection.
- **Add student records** manually for testing purposes.

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
    cd path/to/
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

To run the application:

    ```bash
    python main.py
    ```

## Contributers

- Group 3:
Jin Lee,
Daniar Zhylangozov,
Nadia Chan,
Ziyue Tao
- Contributions to improve the application are welcome. Please feel free to submit a Pull Request.
