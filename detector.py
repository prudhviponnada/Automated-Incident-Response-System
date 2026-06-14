import socket
import time
import json
from datetime import datetime, timezone

def check_port(ip, port):
    """Attempts to connect to the specified IP and Port."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0 

# Reverting to WSL-friendly localhost routing
NODES_TO_MONITOR = [
    {"hostname": "healthy_router", "ip": "127.0.0.1", "port": 8081},
    {"hostname": "failing_router", "ip": "127.0.0.1", "port": 8082}
]

print("Initializing NOC Surveillance...")
print("Starting continuous monitoring loop...")

while True:
    for node in NODES_TO_MONITOR:
        is_up = check_port(node["ip"], node["port"])
        
        if not is_up:
            print(f"\nCRITICAL: {node['hostname']} is DOWN! Generating alert...")
            
            alert_data = {
                "alert_id": f"INC-{int(time.time())}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "hostname": node["hostname"],
                "ip_address": node["ip"],
                "failed_port": node["port"],
                "status": "Unreachable"
            }
            
            with open("active_alert.json", "w") as alert_file:
                json.dump(alert_data, alert_file, indent=4)
            
            print("Alert generated. Halting detection to wait for remediation.")
            exit(1) 
            
    time.sleep(5)
