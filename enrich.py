import json
import requests
import time
import os

# Set your API Key
API_KEY = 'USER-API-KEY'
BASE_URL = 'https://api.legiscan.com/'

# Use absolute paths:
# This gets the directory where the script lives, then looks for 'www' at the parent level
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
PEOPLE_FILE = os.path.join(PROJECT_ROOT, 'www', 'people.json')
OUTPUT_FILE = os.path.join(PROJECT_ROOT, 'www', 'enriched_people.json')

# Load your existing list
with open(PEOPLE_FILE, 'r') as f:
    data = json.load(f)
    people = data['sessionpeople']['people']

enriched_list = []

print(f"Starting enrichment for {len(people)} people...")

for person in people:
    person_id = person['people_id']
    print(f"Fetching details for {person['name']} (ID: {person_id})...")

    # Call the getPerson API
    params = {'key': API_KEY, 'op': 'getPerson', 'id': person_id}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        details = response.json().get('person', {})
        enriched_list.append(details)
    else:
        print(f"Failed to fetch {person['name']}")

    # Rate limiting (1 second delay)
    time.sleep(1)

# Save to the web directory using the absolute path
with open(OUTPUT_FILE, 'w') as f:
    json.dump(enriched_list, f, indent=4)

print(f"Done! Data saved to {OUTPUT_FILE}")
