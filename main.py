from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import pandas as pd
import math

# -----------------------
# App
# -----------------------
app = FastAPI(title="Revenue Monitor API")

# Allow frontend later (localhost web app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later you can restrict to ["http://127.0.0.1:5173", "http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Files
# -----------------------
BASE_DIR = Path(__file__).resolve().parent
KPI_CSV = BASE_DIR / "kpi_metrics_5min.csv"

# -----------------------
# Helpers
# -----------------------
def clean_value(v):
    """Convert NaN/inf to None (JSON-safe)."""
    if v is None:
        return None
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    return v

def clean_records(records: list[dict]) -> list[dict]:
    return [{k: clean_value(v) for k, v in row.items()} for row in records]

# -----------------------
# Routes
# -----------------------
@app.get("/")
def health():
    return {"status": "ok", "service": "revenue-monitor"}

@app.get("/api/kpis/latest")
def latest_kpis(limit: int = 50):
    if not KPI_CSV.exists():
        return {"error": f"File not found: {KPI_CSV.name}"}

    df = pd.read_csv(KPI_CSV)

    # Try to sort by window_start if present
    if "window_start" in df.columns:
        df["window_start"] = pd.to_datetime(df["window_start"], errors="coerce")
        df = df.sort_values("window_start", ascending=False)

    # Convert pandas NaN to Python None safely
    # (still keep our clean_value to handle inf too)
    df = df.where(pd.notnull(df), None)

    # Build response
    limit = max(1, min(limit, 500))  # safety cap
    rows = df.head(limit).to_dict(orient="records")
    rows = clean_records(rows)

    return {
        "rows": rows,
        "count": int(min(limit, len(df))),
        "source": KPI_CSV.name
    }