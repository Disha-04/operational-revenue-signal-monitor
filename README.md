📊 Operational Revenue Signal Monitor

An end-to-end real-time revenue monitoring system that ingests operational data, computes KPI metrics in rolling 5-minute windows, exposes them via a FastAPI backend, and visualizes insights through a premium executive web dashboard and Tableau Public.

This project simulates how modern product, analytics, and operations teams monitor revenue health, SLA breaches, and risk signals in near real time.

🚀 Live Dashboards

🌐 Web Application (FastAPI + HTML/CSS/JS)
	•	Local interactive executive dashboard
	•	Real-time KPI refresh every 5 seconds
	•	WARN / CRIT threshold-based alerting
	•	Revenue trend visualization

  📊 Tableau Executive Dashboard (Public)

🔗 View on Tableau Public:
https://public.tableau.com/views/Book1_17705258725070/Sheet1

Includes:
	•	Revenue trend analysis
	•	Alert status visualization
	•	Payment failure rate
	•	Active users (30-minute window)
	•	Data freshness & SLA insightsKey Features

🔹 Backend (FastAPI)
	•	REST API to serve latest KPI windows
	•	Handles NaN / Inf values safely for JSON responses
	•	CSV-based data ingestion pipeline
	•	Clean API architecture for extensibility

🔹 Frontend (Premium UI)
	•	Executive-grade dark theme dashboard
	•	Live revenue, status, and KPI cards
	•	Interactive revenue trend chart
	•	Configurable WARN / CRIT thresholds
	•	Auto-refresh every 5 seconds

🔹 Analytics & Metrics
	•	Rolling 5-minute KPI windows
	•	Revenue & purchase aggregation
	•	Payment failure rate computation
	•	SLA breach detection (latency + freshness)
	•	Alert classification: OK / WARN / CRIT
  
🧩 Tech Stack
Layer	                  Technology
Backend API             FastAPI, Python
Frontend	              HTML, CSS, JavaScript
Charts	                Chart.js
Analytics	              Pandas
Dashboard	              Tableau Public
Data Store	            CSV (simulated streaming data)
Dev Tools	              Git, GitHub

operational-revenue-signal-monitor/
│
├── app.py                  # FastAPI application
├── event_generator.py      # Simulated event stream
├── metrics_job.py          # KPI computation logic
├── export_to_csv.py        # KPI persistence
├── main.py                 # Orchestration script
│
├── templates/
│   └── index.html          # Executive dashboard UI
│
├── static/
│   └── main.css            # Premium dark theme styling
│
├── raw_events.csv          # Simulated raw events
├── kpi_metrics_5min.csv    # Aggregated KPI windows

How to Run Locally

1️⃣ Clone Repository
git clone https://github.com/Disha-04/operational-revenue-signal-monitor.git
cd operational-revenue-signal-monitor

2️⃣ Create Virtual Environment
python -m venv .venv
source .venv/bin/activate   # macOS / Linux

3️⃣ Install Dependencies
pip install fastapi uvicorn pandas

4️⃣ Start Backend Server
uvicorn app:app --reload

5️⃣ Open Dashboard
http://127.0.0.1:8000



