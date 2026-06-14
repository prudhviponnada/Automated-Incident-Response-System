
# Automated Incident Response System

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
├── docker-compose.yml       # Provisions the simulated network nodes
├── detector.py              # The Watchdog: monitors nodes and generates alerts
├── incident_manager.py      # The Orchestrator: ingests alerts and runs triage
├── active_alert.json        # The dynamic alert payload (generated on failure)
└── incident_response.log    # The system audit trail