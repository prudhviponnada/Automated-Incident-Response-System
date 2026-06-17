import urllib.request
import urllib.error
import time
import json
import subprocess
from datetime import datetime, timezone

NODES_TO_MONITOR = [
    {"hostname": "healthy_router", "url": "http://127.0.0.1:8081"},
    {"hostname": "failing_router", "url": "http://127.0.0.1:8082"}
]

def get_cpu_usage(container_name):
    """Uses docker stats to get current CPU percentage."""
    try:
        result = subprocess.run(
            ['docker', 'stats', '--no-stream', '--format', '{{.CPUPerc}}', container_name],
            capture_output=True, text=True, check=True
        )
        # Convert "100.00%" to a float 100.00
        cpu_str = result.stdout.strip().replace('%', '')
        return float(cpu_str) if cpu_str else 0.0
    except subprocess.CalledProcessError:
        return 0.0

print("Initializing Ultimate NOC Surveillance (HTTP & CPU Layer)...")

while True:
    for node in NODES_TO_MONITOR:
        failure_type = None
        
        # 1. Check CPU Usage
        cpu_usage = get_cpu_usage(node["hostname"])
        if cpu_usage > 80.0:
            print(f"\nCRITICAL: {node['hostname']} CPU is maxed out at {cpu_usage}%! Generating alert...")
            failure_type = "CPU_Spike"
            
        # 2. Check Web Service (Only if CPU is fine)
        if not failure_type:
            try:
                response = urllib.request.urlopen(node["url"], timeout=3)
            except urllib.error.HTTPError as e:
                print(f"\nWARNING: {node['hostname']} returned HTTP {e.code}! Generating alert...")
                failure_type = "App_Error"
            except urllib.error.URLError:
                print(f"\nCRITICAL: {node['hostname']} is DOWN! Generating alert...")
                failure_type = "Node_Offline"

        # 3. Generate Alert if any failure was detected
        if failure_type:
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