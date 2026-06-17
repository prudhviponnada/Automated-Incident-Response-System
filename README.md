import markdown

md_content = """# Automated Incident Response System (WSL2 Edition)

An automated, lightweight Network Operations Center (NOC) orchestrator designed to detect infrastructure failures, generate standard JSON alerts, and perform Level 1 automated triage and zero-touch remediation. 

This project simulates an enterprise SRE/NOC pipeline, bridging the gap between infrastructure monitoring and automated repair, significantly reducing Mean Time To Resolution (MTTR) for critical network incidents.

## 🚀 Key Features
* **Real-time State Monitoring:** Continuously polls target nodes dynamically using internal Docker network IPs, monitoring HTTP response, CPU usage, and network latency.
* **Smart Decision Engine:** Automatically classifies incidents into four distinct failure types (Node Offline, App Error, CPU Spike, High Latency) and routes them to the correct remediation playbook.
* **JSON Alert Generation:** Automatically structures failure data into standard JSON payloads mimicking enterprise webhook alerts.
* **Zero-Touch Remediation:** Integrates with Ansible to execute specific recovery playbooks the moment a failure is verified, eliminating manual NOC investigation time.
* **Automated Post-Mortem Reporting:** Generates a timestamped text report for every resolved incident, calculating the exact MTTR (Mean Time To Resolution) for SLA compliance.

## 🛠️ Tech Stack
* **Language:** Python 3
* **Infrastructure:** Docker & Docker Compose
* **Configuration Management:** Ansible
* **System Automation:** `subprocess` module for native OS and Container Engine interaction

## 📂 Project Structure
Code output
README files generated successfully.

```text
├── docker-compose.yml       # Provisions the simulated network nodes
├── detector.py              # The Watchdog: monitors nodes, CPU, and latency
├── incident_manager.py      # The Master Orchestrator: routes alerts to Ansible
├── remediate.yml            # Playbook: Fixes complete node outages
├── remediate_app.yml        # Playbook: Fixes HTTP 500 / Config corruption
├── remediate_cpu.yml        # Playbook: Fixes 100% Resource Exhaustion
├── remediate_network.yml    # Playbook: Fixes Latency/QoS degradation
├── active_alert.json        # The dynamic alert payload (generated dynamically)
└── incident_response.log    # The system audit trail (generated dynamically)
```
⚙️ Installation & Prerequisites
You will need Python 3.x, Docker Desktop (with WSL2 Integration), and Ansible installed on your system.

Clone this repository to your local machine.
Navigate to the project directory:

Bash
cd Automated-Incident-Response-System
Spin up the simulated network environment:

Bash
docker compose up -d
💻 Usage & Demonstration
To see the automated incident lifecycle in action, you will need to open three separate terminal windows.

Terminal 1: Start the Master Orchestrator
This script acts as the automated NOC agent, waiting for alerts.

Bash
python3 incident_manager.py
Terminal 2: Start the Watchdog
This script continuously surveys the network environment.

Bash
python3 detector.py
🧪 Testing the 4 Failure Scenarios
In your Terminal 3, you can intentionally break the infrastructure using any of the following commands. Watch Terminal 1 and 2 to see the system detect, classify, and automatically fix the issue within seconds.

Scenario 1: Node Offline (Hard Down)
Simulates a complete hardware or power failure.

Bash
docker stop failing_router
Scenario 2: Application Error (Grey Failure)
Simulates a developer pushing a corrupt Nginx configuration, causing HTTP 500 errors.

Bash
docker exec failing_router sh -c "echo 'events {} http { server { listen 80; location / { return 500; } } }' > /etc/nginx/nginx.conf && nginx -s reload"
Scenario 3: Resource Exhaustion (CPU Spike)
Injects an infinite loop to max out the container's CPU at 100%.

Bash
docker exec -d failing_router sh -c "while true; do true; done"
Scenario 4: High Latency (The WSL2 Workaround)
Architectural Note: Because the WSL2 kernel lacks the netem traffic control module for Layer-3 shaping, this scenario simulates congestion at Layer-7 by injecting a custom Python HTTP server that intentionally delays responses by 3 seconds, triggering the 1.5s SLA violation.

Bash
docker exec -d failing_router sh -c "apk add --no-cache python3 && nginx -s quit && python3 -c 'import time, http.server; class S(http.server.SimpleHTTPRequestHandler): \n def do_GET(self): time.sleep(3); self.send_response(200); self.end_headers()\nhttp.server.HTTPServer((\"\", 80), S).serve_forever()'"
📊 Expected Output & Reporting
Once any failure is triggered:

detector.py immediately identifies the drop, classifies the failure type, writes active_alert.json, and halts.

incident_manager.py detects the JSON payload, reads the failure_type, and triggers the corresponding Ansible playbook.

Ansible repairs the node.

The Orchestrator generates a specific Post-Mortem Report (e.g., report_INC-123456.txt) documenting the exact Mean Time To Resolution (MTTR).

DROP YOUR VALUABLE FEEDBACK, I'M OPEN TO SUGGESTIONS!
