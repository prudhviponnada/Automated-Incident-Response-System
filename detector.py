import urllib.request
import urllib.error
import time
import json
from datetime import datetime, timezone

NODES_TO_MONITOR = [
    {"hostname": "healthy_router", "url": "http://127.0.0.1:8081"},
    {"hostname": "failing_router", "url": "http://127.0.0.1:8082"}
]

print("Initializing Advanced NOC Surveillance (HTTP Layer)...")

while True:
    for node in NODES_TO_MONITOR:
        try:
            # Try to load the webpage
            response = urllib.request.urlopen(node["url"], timeout=3)
            # If we get here, the page loaded (HTTP 200 OK)
            continue 
            
        except urllib.error.HTTPError as e:
            # The server is UP, but returning a broken page (e.g., 500 Internal Server Error)
            print(f"\nWARNING: {node['hostname']} returned HTTP {e.code}! Generating alert...")
            failure_type = "App_Error"
            
        except urllib.error.URLError:
            # The server is completely OFF
            print(f"\nCRITICAL: {node['hostname']} is DOWN! Generating alert...")
            failure_type = "Node_Offline"

        # Generate the payload
        alert_data = {
            "alert_id": f"INC-{int(time.time())}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "hostname": node["hostname"],
            "failure_type": failure_type
        }
        
        with open("active_alert.json", "w") as alert_file:
            json.dump(alert_data, alert_file, indent=4)
        
        print("Alert generated. Halting detection to wait for remediation.")
        exit(1) 
            
    time.sleep(5)