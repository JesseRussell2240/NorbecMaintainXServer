from pylogix import PLC
import time

# Define PLC connection details
PLC_IP = '10.10.0.10'  

# Define the tags to monitor
tags_to_monitor = [
    'SAIP_Request_Pentane_Circulation',
    'SAIP_Request_ISO_FillingDayTank',
    'SAIP_Request_POLY1_FillingDayTank',
    'ISO_transfer',
    'SAIP_Request_POLY1_FillingDayTank'
]

# Initialize a dictionary to store the last known value of each tag
last_values = {tag: None for tag in tags_to_monitor}

# Function to check and print if any tag value changes and inital conditions
def check_tag_values():
    with PLC() as comm:
        comm.IPAddress = PLC_IP
        
        for tag in tags_to_monitor:
            # Read the current value of the tag
            result = comm.Read(tag)
            
            if result.Status == 'Success':
                # Check if the value has changed
                if last_values[tag] is None:
                    last_values[tag] = result.Value  # Initialize the first value
                    print(f"Tag '{tag}' read initally as: {last_values[tag]} -> {result.Value}")
                elif result.Value != last_values[tag]:
                    print(f"Tag '{tag}' changed: {last_values[tag]} -> {result.Value}")
                    last_values[tag] = result.Value  # Update the last known value
            else:
                print(f"Error reading tag '{tag}': {result.Status}")

# Main loop to check values periodically 2 times per second
try:
    
    while True:
        check_tag_values()        
        time.sleep(0.5)  #
except KeyboardInterrupt:
    print("Monitoring stopped.")
