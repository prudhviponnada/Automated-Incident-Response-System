import json
import os
import time
import subprocess
import logging

logging.basicConfig(
    filename='incident_response.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

ALERT_FILE = "active_alert.json"

def run_diagnostic_check(hostname):
    """Simulates a ping by checking if the container is actively running."""
    logging.info(f"Starting Level 1 Triage: Checking host state for {hostname}")
    
    try:
        # Ask Docker if the container's state is 'Running'
        result = subprocess.run(
            ['docker', 'inspect', '-f', '{{.State.Running}}', hostname],
            capture_output=True, text=True, check=True
        )
        is_running = result.stdout.strip()
        
        if is_running == "true":
            logging.info("Level 1 Triage Result: Host is powered ON. The OS is alive, but the web service crashed.")
            return "Service Down (OS Alive)"
        else:
            logging.critical("Level 1 Triage Result: Host is completely powered OFF. Node is offline.")
            return "Node Offline"
    except subprocess.CalledProcessError:
        logging.critical("Level 1 Triage Result: Host does not exist or is unreachable.")
        return "Node Unreachable"

print("Incident Manager started. Waiting for alerts...")

while True:
    if os.path.exists(ALERT_FILE):
        print("\n[!] ALERT DETECTED! Initiating automated response...")
        logging.info("--- NEW INCIDENT DETECTED ---")
        
        with open(ALERT_FILE, 'r') as f:
            alert_data = json.load(f)
            
        incident_id = alert_data.get('alert_id')
        hostname = alert_data.get('hostname')
        failed_port = alert_data.get('failed_port')
        
        logging.info(f"Alert ID: {incident_id} | Hostname: {hostname} | Failed Port: {failed_port}")
        
        # Pass the hostname instead of the IP for the Docker check
        triage_status = run_diagnostic_check(hostname)
        
        print(f"Diagnostics complete: {triage_status}")
        print("Check incident_response.log for details.")
        
        os.remove(ALERT_FILE)
        logging.info("Alert payload processed and removed.")
        logging.info("--- INCIDENT PAUSED PENDING REMEDIATION (PHASE 3) ---")
        
        print("Awaiting next alert...\n")
        
    time.sleep(3)
