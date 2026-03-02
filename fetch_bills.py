import requests
import json
import os

# IMPORTANT: Replace this placeholder with your actual LegiScan API key
API_KEY = "USER-API-KEY"
STATE = "MO"
# This file is saved where your Nginx web server can serve it
OUTPUT_FILE = "/home/dietpi/civic-portal/www/data.json"

def fetch_bills():
    # LegiScan API Endpoint to get the Master List for Missouri
    url = f"https://api.legiscan.com/?key={API_KEY}&op=getMasterList&state={STATE}"

    try:
        print(f"Fetching data from LegiScan for {STATE}...")
        response = requests.get(url)
        response.raise_for_status() # Raises an error for bad HTTP responses

        # Save the JSON response locally
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(response.json(), f, indent=4)

        print(f"Success: Data successfully updated to /www/data.json")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_bills()
