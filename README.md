# 📊 Operational Revenue Signal Monitor

An end-to-end **near real-time revenue monitoring system** that simulates event ingestion, computes KPI metrics in rolling **5-minute windows**, exposes them via a **FastAPI backend**, and visualizes insights through a **premium executive web dashboard** and **Tableau Public**.

This project mirrors how modern Product/Analytics/Operations teams monitor **revenue health, SLA breaches, and risk signals** in production.

---

## 🚀 Live Dashboards

### 🌐 Web Dashboard (FastAPI + HTML/CSS/JS)
- Executive-style dashboard UI (premium dark theme)
- Auto-refresh KPI feed every **5 seconds**
- Threshold-based alerting: **OK / WARN / CRIT**
- Revenue trend visualization (Chart.js)

> **Local URL:** `http://127.0.0.1:8000`

### 📊 Tableau Executive Dashboard (Public)
🔗 **Tableau Public:**  
https://public.tableau.com/views/Book1_17705258725070/Sheet1

Includes:
- Revenue trend analysis  
- Alert status visualization  
- Payment failure rate  
- Active users (30-minute window)  
- Data freshness & SLA insights  

---

## 🎥 Demo

## 🖼️ Dashboard Previews

### 🌐 Web Dashboard (FastAPI + Premium UI)
![Web Dashboard Preview](Web%20Dashboard.png)

### 📊 Tableau Executive Dashboard
![Tableau Dashboard Preview](Tableau%20Dashboard.png)



---

## ✨ Key Features

### 🔹 Backend (FastAPI)
- REST API to serve latest KPI windows
- Handles `NaN / Inf` safely for JSON responses
- CSV-based ingestion pipeline (simulated streaming)
- Clean structure for extensibility

### 🔹 Frontend (Premium UI)
- Executive-grade dark theme dashboard
- KPI cards: **Revenue / Status / Rows**
- Interactive revenue trend chart (Chart.js)
- Configurable WARN/CRIT thresholds
- Auto refresh every 5 seconds

### 🔹 Analytics & Metrics
- Rolling 5-minute KPI windows
- Revenue & purchase aggregation
- Payment failure rate computation
- SLA breach detection (latency + freshness)
- Alert classification: **OK / WARN / CRIT**

---

## 🧩 Tech Stack

| Layer | Technology |
|------|------------|
| Backend API | FastAPI, Python |
| Frontend | HTML, CSS, JavaScript |
| Charts | Chart.js |
| Analytics | Pandas |
| Dashboard | Tableau Public |
| Data Store | CSV (simulated streaming data) |
| Dev Tools | Git, GitHub |

---

## 📁 Project Structure

```bash
operational-revenue-signal-monitor/
├── app.py                  # FastAPI application
├── event_generator.py      # Simulated event stream
├── metrics_job.py          # KPI computation logic
├── export_to_csv.py        # KPI persistence
├── main.py                 # Orchestration script
├── templates/
│   └── index.html          # Executive dashboard UI
├── static/
│   └── main.css            # Premium dark theme styling
├── raw_events.csv          # Simulated raw events
├── kpi_metrics_5min.csv    # Aggregated KPI windows
└── assets/                 # (optional) screenshots / GIFs

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



