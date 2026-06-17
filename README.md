# Automated Incident Response System for WSL2

An automated, lightweight Network Operations Center (NOC) orchestrator designed to detect infrastructure failures, generate standard JSON alerts, and perform Level 1 automated triage. 

This project simulates an enterprise alerting pipeline, bridging the gap between infrastructure monitoring and automated remediation, significantly reducing Mean Time To Resolution (MTTR) for critical network incidents.

## 🚀 Key Features

* **Real-time State Monitoring:** Continuously polls target nodes dynamically using internal Docker network IPs.
* **JSON Alert Generation:** Automatically structures failure data into standard JSON payloads mimicking enterprise webhook alerts.
* **Zero-Touch Triage:** Executes Level 1 diagnostic checks (e.g., system power state verification) the moment an alert is detected, eliminating manual NOC investigation time.
* **Decoupled Architecture:** Utilizes a microservices approach where detection (`detector.py`) and orchestration (`incident_manager.py`) operate independently via a file-based queue.
* **Audit Logging:** Maintains professional, timestamped logs of all incident states and automated actions.

## 🛠️ Tech Stack

* **Language:** Python 3
* **Infrastructure:** Docker & Docker Compose
* **System Automation:** `subprocess` module for native OS and Container Engine interaction
* **Logging:** Standard Python `logging` library

## 📂 Project Structure

```text
├── docker-compose.yml       # Provisions the simulated network nodes
├── detector.py              # The Watchdog: monitors nodes and generates alerts
├── incident_manager.py      # The Orchestrator: ingests alerts and runs triage
├── active_alert.json        # The dynamic alert payload (generated on failure)
└── incident_response.log    # The system audit trail
```
## ⚙️  ** Installation & Prerequisites**
* You will need Python 3.x and Docker installed on your system.

* Clone this repository to your local machine.

* Navigate to the project directory:

# **Bash**
```text
cd Automated Incident Response System for WSL2
```
Spin up the simulated network environment:

# **Bash**
```text
docker compose up -d
```
## 💻  **Usage & Demonstration**
To see the automated incident lifecycle in action, you will need to open three separate terminal windows.

* Terminal 1: Start the Orchestrator
This script acts as the automated NOC agent, waiting for alerts.

# Terminal 1: start the Master Orchestrator **Bash**
```text
python3 incident_manager.py
```


# Terminal 2: start watchdog 
Start the Detector.
This script continuously surveys the network environment.
```text
python3 detector.py
```

# Terminal 3:**Bash**
Trigger a Simulated Outage. 
Scenario 1: Node Offline (Hard Down). Crash the simulated router to trigger the incident response pipeline:

```text
docker stop failing_router

```
Scenario 2: Application Error (Grey Failure)

Simulates a developer pushing a corrupt Nginx configuration, causing HTTP 500 errors.
```text
docker exec failing_router sh -c "echo 'events {} http { server { listen 80; location / { return 500; } } }' > /etc/nginx/nginx.conf && nginx -s reload"

```
Scenario 3: Resource Exhaustion (CPU Spike)

Injects an infinite loop to max out the container's CPU at 100%.
```text
docker exec -d failing_router sh -c "while true; do true; done"

```
Scenario 4: High Latency (The WSL2 Workaround)

Architectural Note: Because the WSL2 kernel lacks the netem traffic control module for Layer-3 shaping, this scenario simulates congestion at Layer-7 by injecting a custom Python HTTP server that intentionally delays responses by 3 seconds, triggering the 1.5s SLA violation.
```text
docker exec -d failing_router sh -c "apk add --no-cache python3 && nginx -s quit && python3 -c 'import time, http.server; class S(http.server.SimpleHTTPRequestHandler): \n def do_GET(self): time.sleep(3); self.send_response(200); self.end_headers()\nhttp.server.HTTPServer((\"\", 80), S).serve_forever()'"

```
## **Expected Output & Reporting**
Once the failure is triggered:

1. detector.py immediately identifies the drop, classifies the failure type, writes active_alert.json, and halts.

2.  incident_manager.py detects the JSON payload, reads the failure_type, and triggers the corresponding Ansible playbook.

3. Ansible repairs the node.

4. The Orchestrator generates a specific Post-Mortem Report (e.g., report_INC-123456.txt) documenting the exact Mean Time To Resolution (MTTR).
 
    ## DROP YOUR VALUABLE FEEDBACK I'M OPEN TO SUGGESTIONS ##
