
import time
import requests
from pylogix import PLC
import json
import os
import random
import subprocess
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
import Database  # Sensor config

# Load environment variables
load_dotenv()
BEARER_TOKEN = os.getenv("MAINTAINX_API_KEY")
BASE_URL = 'https://api.getmaintainx.com/v1/meterreadings'

PLC_IP = '10.10.0.10'
PLC_PORT = 44818  # Default for Rockwell PLCs

USB_MOUNT_PATH = "/media/logusb"
USB_LOG_FILE = os.path.join(USB_MOUNT_PATH, "maintainx.log")

# Setup logging to USB with rotation (latest 500 messages)
if os.path.ismount(USB_MOUNT_PATH):
    log_handler = RotatingFileHandler(
        USB_LOG_FILE, maxBytes=50000, backupCount=1
    )
    logging.basicConfig(
        handlers=[log_handler],
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    logging.info("Logging initialized to USB.")
else:
    logging.basicConfig(level=logging.INFO)
    logging.warning("USB drive not mounted. Logging to console only.")

def switch_network(interface, state):
    try:
        subprocess.run(["sudo", "ip", "link", "set", interface, state], check=True)
        logging.info(f"Network {interface} set {state}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to switch {interface} {state}: {e}")

def readPLCsensor(tag_name):
    try:
        plc = PLC()
        plc.IPAddress = PLC_IP
        plc.Port = PLC_PORT
        tag_value = plc.Read(tag_name)

        if tag_value.Value is True:
            return 1
        elif tag_value.Value is False:
            return 0
        return tag_value.Value
    except Exception as e:
        logging.error(f"Error reading from PLC sensor for tag '{tag_name}': {e}")
        return None

def get_rate_limits(response):
    try:
        rate_limit = int(response.headers.get("X-Rate-Limit-Limit", 100))
        remaining = int(response.headers.get("X-Rate-Limit-Remaining", 1))
        reset = int(response.headers.get("X-Rate-Limit-Reset", 60))
        return rate_limit, remaining, reset
    except Exception as e:
        logging.warning(f"Error reading rate limit headers: {e}")
        return 100, 1, 60

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
                logging.info(f"Meter {meter_id} → Value {value} POST success.")
                return remaining, reset
            elif response.status_code == 429:
                logging.warning(f"Rate limit exceeded. Waiting {reset}s...")
                time.sleep(reset + 1)
            else:
                logging.error(f"Failed POST for {meter_id}: {response.status_code}, {response.text}")
                return remaining, reset
        except Exception as e:
            logging.error(f"POST error: {e}")
            return 1, 60

def update_all_sensors():
    sensors = Database.database["sensors"]
    for sensor in sensors:
        tag_name = sensor["data"].get("tag_name")
        if tag_name and tag_name != "TBD":
            reading = readPLCsensor(tag_name)
            sensor["data"]["current_reading"] = reading
            logging.info(f"Read {sensor['category']} at {sensor['location']} [{tag_name}] → {reading}")
        else:
            logging.info(f"Skipped sensor {sensor['location']} - no valid tag")

def send_all_sensor_data():
    sensors = Database.database["sensors"]
    remaining, reset = 100, 60
    for sensor in sensors:
        data = sensor["data"]
        current = data.get("current_reading")
        last = data.get("last_sent_reading")
        if current is not None and current != last:
            meter_id = data.get("meter_id")
            remaining, reset = POSTdata(meter_id, current)
            data["last_sent_reading"] = current
            if remaining == 0:
                logging.info("Hit rate limit, sleeping...")
                time.sleep(reset + 1)
        else:
            logging.info(f"Skipped POST for {data.get('tag_name')} (no change).")

def main():
    while True:
        switch_network("eth0", "up")
        switch_network("eth1", "down")
        time.sleep(70)

        update_all_sensors()

        switch_network("eth0", "down")
        switch_network("eth1", "up")
        time.sleep(70)

        send_all_sensor_data()
        time.sleep(70)

if __name__ == "__main__":
    main()
