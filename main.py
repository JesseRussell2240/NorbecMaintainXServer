import time
import requests
from pylogix import PLC
import json
import os
import random
import Database  # Importing the database module

from dotenv import load_dotenv
load_dotenv()
BEARER_TOKEN = os.getenv("MAINTAINX_API_KEY") #access a local .env file to get tokin


# Define the base URL and the Bearer Token for authentication
BASE_URL = 'https://api.getmaintainx.com/v1/meterreadings'

# Define PLC connection details
PLC_IP = '10.10.0.10'
PLC_PORT = 44818  # Default for Rockwell PLCs


import subprocess

def switch_network(interface, state):
    try:
        subprocess.run(["sudo", "ip", "link", "set", interface, state], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to switch {interface} {state}: {e}")


# Helper function to read data from the PLC sensor
def readPLCsensor(tag_name):
    try:
        plc = PLC()
        plc.IPAddress = PLC_IP
        plc.Port = PLC_PORT
        tag_value = plc.Read(tag_name)

        # Check if the value is "False" or "True" and convert to 0 or 1
        if tag_value.Value == False:
            tag_value.Value = 0
        elif tag_value.Value == True:
            tag_value.Value = 1
        
        # temp code for testing
        #tag_value.Value = random.randint(0,10)
        
        return tag_value.Value
    except Exception as e:
        print(f"Error reading from PLC sensor for tag '{tag_name}': {e}")
        return None

def get_rate_limits(response):
    """Extract rate limit values from API response headers."""
    try:
        rate_limit = int(response.headers.get("X-Rate-Limit-Limit", 100))
        remaining = int(response.headers.get("X-Rate-Limit-Remaining", 1))
        reset = int(response.headers.get("X-Rate-Limit-Reset", 60))
        return rate_limit, remaining, reset
    except Exception as e:
        print(f"Error reading rate limit headers: {e}")
        return 100, 1, 60  # Default values


def POSTdata(meter_id, value):
    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = json.dumps([{"meterId": meter_id, "value": value}])
    
    while True:
        try:
            response = requests.post(BASE_URL, headers=headers, data=payload, timeout=10)
            rate_limit, remaining, reset = get_rate_limits(response)
            
            if response.status_code in [200, 201]:
                print(f"Data for meter {meter_id} sent successfully!")
                return remaining, reset
            elif response.status_code == 429:
                print(f"Rate limit exceeded. Waiting {reset} seconds...")
                time.sleep(reset + 1)
            else:
                print(f"Failed to send data for meter {meter_id}: {response.status_code}, {response.text}")
                return remaining, reset
        except Exception as e:
            print(f"Error in POST to API: {e}")
            return 1, 60  # Default retry time

def update_all_sensors():
    sensors = Database.database["sensors"]
    for sensor in sensors:
        tag_name = sensor["data"].get("tag_name")

        if tag_name and tag_name != "TBD":
            reading = readPLCsensor(tag_name)
            sensor["data"]["current_reading"] = reading  # Store the new reading
            print(f"Updated {sensor['category']} sensor at '{sensor['location']}' ({sensor['parameter']}) "
                  f"[Tag: {tag_name}] -> New Value: {reading}")
        else:
            print(f"Skipping {sensor['category']} sensor at '{sensor['location']}' ({sensor['parameter']}) "
                  f"[Tag: {tag_name}] - No valid tag assigned")

def send_all_sensor_data():
    sensors = Database.database["sensors"]
    remaining, reset = 100, 60  # Default values
    for sensor in sensors:
        data = sensor["data"]
        tag_name = data.get("tag_name")
        current_value = data.get("current_reading")
        last_sent_value = data.get("last_sent_reading")
        
        if tag_name and current_value is not None:
            if current_value != last_sent_value:
                meter_id = data.get("meter_id")
                remaining, reset = POSTdata(meter_id, current_value)
                data["last_sent_reading"] = current_value
                
                if remaining == 0:
                    print(f"Rate limit reached, waiting {reset} seconds...")
                    time.sleep(reset + 1)
            else:
                print(f"Skipping POST for {tag_name}: No change in value ({current_value}).")



# Main function
def main():
    while True:
        
        
        #eth1 is USB ether net card
        #eth0 is port on r-pi
        #use adapter for outside connection
        #use r-pi for PLC network
        switch_network("eth0", "up")
        switch_network("eth1", "down")
        time.sleep(70)
        
        # Update all sensor values from the PLC
        update_all_sensors()

        switch_network("eth0", "down")
        switch_network("eth1", "up")
        time.sleep(70)

        # Send all sensor data to the API via POST
        send_all_sensor_data()
        
        time.sleep(70)
        
        


if __name__ == "__main__":
    main()
