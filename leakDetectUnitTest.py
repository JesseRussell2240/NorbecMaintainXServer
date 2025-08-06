import time
from pylogix import PLC
from LeakDatabase import get_leak_detectors

# Define the PLC connection details
PLC_IP = '10.10.0.10'
PLC_PORT = 44818  # Default for Rockwell PLCs, adjust as needed

# Helper function to read data from the PLC sensor
def readPLCsensor(tag_name):
    try:
        plc = PLC()
        plc.IPAddress = PLC_IP
        plc.Port = PLC_PORT
        tag_value = plc.Read(tag_name)
        
        if tag_value.Status != 'Success':
            print(f"PLC read failed for {tag_name}. Status: {tag_value.Status}")
            return None
        
        return tag_value.Value  # Assuming the value is a boolean or integer (0/1)
    except Exception as e:
        print(f"Error reading from PLC sensor for tag '{tag_name}': {e}")
        return None

# Main function to communicate with PLC and print True/False for each leak detector
def main():
    # Get leak detectors from the database
    leak_detectors = get_leak_detectors()

    # Iterate through all leak detectors in the database
    for category, detectors in leak_detectors.items():
        print(f"Processing {category}:")
        
        for detector_name, detector_info in detectors.items():
            tag_name = detector_info["tag_name"]
            print(f"Reading sensor for {detector_name} ({tag_name})")

            # Read the sensor value from the PLC
            sensor_value = readPLCsensor(tag_name)
            
            if sensor_value is None:
                print(f"{detector_name} (Tag: {tag_name}) - Error reading PLC sensor")
            else:
                # Assuming 0 means False (inactive) and non-zero means True (active)
                print(f"{detector_name} (Tag: {tag_name}) - {'True' if sensor_value else 'False'}")

            time.sleep(0.1)  # Small pause to avoid rapid requests to the PLC

if __name__ == "__main__":
    while True:
        main()
