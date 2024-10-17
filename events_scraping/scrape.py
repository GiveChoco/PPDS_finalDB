import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import json

load_dotenv()
API_KEY = os.getenv("API_KEY")


# Uncomment code below if you wish to see the process of scraping data.
# It is commented out because scraping takes >8 minutes.
# All scraped data is stored in the csv file in this directory.

# Initialize a Chrome WebDriver instance to interact with the website
driver = webdriver.Chrome()

driver.get("https://engage.nyu.edu/events")

time.sleep(2)  # Pause to allow the page to load

events_count_soup = BeautifulSoup(driver.page_source, 'html.parser')
all_events_count = events_count_soup.find("div", attrs={"style": "color: rgb(73, 73, 73); margin: 15px 0px 0px; font-style: italic; text-align: left;"})
match = re.search(r"\d{4}", all_events_count.text)
all_events_count_number = 0

if match:
    all_events_count_number = int(match.group())
    print(all_events_count_number)  
else:
    print("No 4-digit number found.")

count = (all_events_count_number // 15) + 1 #events are loaded 15 events at a time. So when we click a "load more" button, 15 new events will show up
                                    # Thus, to click the right amount of time, we need this count variable


# # List to store product data scraped from the website
event_data = []
pattern = re.compile(r'/event/(\d+)')  # Regular expression to match event links

# # Function to scrape data from the current page's product links
def request_pages(links):
    base_url = "https://engage.nyu.edu"  # Base API URL
    events_data = []  # List to store the desired event data
    
    for link in links:
        # Construct the full API URL
        full_url = base_url + link
        
        try:
            # Send GET request
            response = requests.get(full_url)
            
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the response with BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find the script tag containing 'window.initialAppState'
                # script_tag = soup.find('script', text=lambda t: 'window.initialAppState' in t)
                script_tag = soup.find('script', string=re.compile(r'window\.initialAppState'))

                if script_tag:
                    # Extract the script content and find the JSON-like structure
                    script_content = script_tag.string.strip()
                    start_index = script_content.find('{')
                    end_index = script_content.rfind('}')  # Find the last closing bracket
                    json_str = script_content[start_index:end_index+1]
                    
                    # Parse the JSON-like string into a Python dictionary
                    dict_data = json.loads(json_str)
                    
                    # Access elements from the dictionary
                    event_dict = dict_data["preFetchedData"]['event']
                    
                    # # Extract the desired data
                    # categories = event_dict['theme']
                    # category_names = [category.get('name', '') for category in categories]
                    categories = event_dict['categories']
                    category_array = []
                    for i in range(len(categories)):
                        category_array.append(categories[i]['name'])


                    event_info = {
                        'id': event_dict['id'],
                        'name': event_dict['name'],
                        # 'categories': category_names,
                        'startsOn': event_dict['startsOn'],
                        'endsOn': event_dict['endsOn'],
                        'venue': event_dict['address']['name'],
                        'theme': event_dict['theme'],
                        'categories': category_array,
                        'description': event_dict['description'],
                    }
                    
                    event_id = event_dict['id']
                    print(f'parsed {event_id}')
                    # Add the event info to the list
                    events_data.append(event_info)
                
            else:
                print(f"Failed request for {full_url}, Status code: {response.status_code}")
        
        except Exception as e:
            print(f"Error occurred for {full_url}: {e}")
    
    return events_data  # Return the list of extracted event data


# Function to navigate to the next page of products
def load_more():
    try:
        # Find the parent div with class 'outlinedButton' and its immediate child button using CSS selector
        load_more_button = driver.find_element(By.CSS_SELECTOR, "div.outlinedButton > button")

        # Use JavaScript to click the button
        driver.execute_script("arguments[0].click();", load_more_button)
        return True  # Success, moved to the next page
    except Exception as e:
        print(f"Failed to click next button: {e}")
        return False  # Failed to move to the next page

    
while (count > 0):
    load_more()
    count -= 10
    time.sleep(0.5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
event_link_tags = soup.find_all("a", attrs={"style": 'text-decoration: none;'})
event_links = []

for tag in event_link_tags:
    href = tag['href']
    match = pattern.search(href)
    if match:
        event_links.append(match.group())


result = request_pages(event_links)

# # Save the scraped product data to a CSV file
df = pd.DataFrame(result)
df.to_csv('events.csv', index=False)  