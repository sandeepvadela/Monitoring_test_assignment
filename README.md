# Monitoring_test_assignment 

# Task 3.2 – Real-Time Transaction Monitoring System

## Overview
This project implements a real-time transaction monitoring system that ingests transaction data, detects anomalies, and provides a live dashboard for visualization and alerting.

**Main files:**
- `analyze_data.py` – Data analysis and threshold selection
- `monitoring_file.py` – Main Flask application (API, anomaly detection, dashboard backend)
- `dashboard.html` – Dashboard template (to be placed in a `templates` folder)

---


###  Install Required Python Packages

Open a terminal/command prompt in your project directory and run:
```sh
pip install flask pandas matplotlib seaborn
```
These packages are required for data analysis, visualization, and running the web application.

---

##  Project Structure

Your project directory should look like this:
```
your_project/
├── analyze_data.py
├── monitoring_file.py 
└── templates/
    └── dashboard.html
```

---

## Step-by-Step Implementation 

### Step 1: Preparing my  Data
1. Placed my csv files ( `transactions.csv`, `transactions_auth_codes.csv`) in the project directory.
2. These files will be used for data analysis and threshold selection.

### Step 2: Analyzed Data and Set Thresholds
1. Run the data analysis script to explore the data and determine thresholds:
   ```sh
   python analyze_data.py
   ```
2. The script will:
   - Load and explore the data
   - Calculate statistics (mean, std, etc.) for each transaction status
   - Suggest thresholds for failed, denied, reversed, and approved transactions
3. **Why:** This ensures the monitoring system uses data-driven, justifiable thresholds for detecting anomalies.

### Step 3: Setting Up the Monitoring System
1. I have a directory structure  with `monitoring_file.py` and a `templates` folder containing `dashboard.html`.

### Step 4: Running the Monitoring System
1. Path to the project
   ```sh
   cd path/to/your_project
   ```
2. Start the Flask app:
   ```sh
   python monitoring_file.py
   ```
3. The server will start and listen on `http://localhost:8080` by default.

### Step 5: Using a  Real-Time Dashboard
1. Open your web browser and go to:
   [http://localhost:8080](http://localhost:8080)
2. The dashboard will display:
   - Live transaction counts by status (approved, failed, denied, reversed)
   - Recent transactions
   - Test buttons to simulate different transaction scenarios
   - System thresholds and API endpoint documentation
3. The dashboard auto-refreshes every 5 seconds for real-time updates.

### Step 6: Testing  the System
1. Use the test buttons on the dashboard to send sample transactions.
2. Observe real-time updates and alerts on the dashboard and in the console.

### Step 7: API Endpoints (for Integration or Demo)
- `POST /api/transaction` – Receives transaction data (timestamp, status, count)
- `GET /api/transactions` – Returns recent transactions
- `GET /api/stats` – Returns statistics and thresholds
- `GET /api/health` – Health check endpoint

### Step 8: How Anomaly Detection Works
- The system uses rule-based thresholds (from your data analysis) to detect anomalies in real time.
- Alerts are triggered in the console when thresholds are breached (e.g., failed > 5, denied > 10, etc.).
- The alerting logic can be extended to send notifications via email, Slack, etc.

---

## Insights from Each File

### 1. `analyze_data.py`
- **Purpose:** Analyze historical transaction data to understand normal patterns and set thresholds for anomaly detection.
- **Insights:**
  - Identified typical transaction volumes for each status (approved, failed, denied, reversed).
  - Calculated statistical baselines (mean, std) and recommended thresholds (e.g., failed > 5, denied > 10).
  - Detected periods with spikes in failed/denied transactions and low approved transactions.
  - Found that spikes in certain authorization codes (like "51") may indicate broader issues.

### 2. `monitoring_file.py`
- **Purpose:** Implements the real-time monitoring system, including API endpoints, anomaly detection, alerting, and dashboard serving.
- **Insights:**
  - Successfully detects and alerts on abnormal transaction patterns in real time.
  - API endpoints reliably receive and process transaction data.
  - Maintains a rolling window of recent transactions for efficient monitoring.
  - Alerting logic is modular and can be extended for more advanced notifications.
  - System is lightweight, robust, and suitable for real-time use.

### 3. `dashboard.html`
- **Purpose:** Provides a user-friendly, real-time web dashboard for monitoring transaction status and alerts.
- **Insights:**
  - Displays live transaction counts and recent transactions with clear status indicators.
  - Test buttons allow simulation of different transaction scenarios.
  - Auto-refreshes every 5 seconds for real-time visibility.
  - Interface is clean, intuitive, and highlights anomalies as they occur.
  - System thresholds and API documentation are visible for transparency.

---

---

