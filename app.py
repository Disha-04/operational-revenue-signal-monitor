# app.py
from pathlib import Path
import math
import pandas as pd
import numpy as np

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
KPI_CSV = BASE_DIR / "kpi_metrics_5min.csv"

app = FastAPI(title="Operational Revenue Signal Monitor")

# Allow browser to call /api endpoints (safe for localhost dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static + Templates
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def sanitize_for_json(df: pd.DataFrame) -> pd.DataFrame:
    """
    Make dataframe safe for JSON:
    - inf/-inf -> NaN
    - NaN/NA -> None
    """
    df = df.copy()

    # ensure we can store Python None in numeric columns
    df = df.astype(object)

    # convert inf to NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # convert NaN/NA to None
    df = df.where(pd.notnull(df), None)

    return df


@app.get("/health")
def health():
    return {"status": "ok", "service": "revenue-monitor"}


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    # renders templates/index.html
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/kpis/latest")
def latest_kpis(limit: int = 50):
    if not KPI_CSV.exists():
        return {
            "rows": [],
            "count": 0,
            "source": KPI_CSV.name,
            "error": f"File not found: {KPI_CSV.name}",
        }

    df = pd.read_csv(KPI_CSV)

    # Sort by window_start if present
    if "window_start" in df.columns:
        df["_ws"] = pd.to_datetime(df["window_start"], errors="coerce")
        df = df.sort_values("_ws", ascending=False).drop(columns=["_ws"])

    df = df.head(int(limit))

    # ✅ critical: remove NaN/Inf before converting to dict
    df = sanitize_for_json(df)

    return {
        "rows": df.to_dict(orient="records"),
        "count": int(len(df)),
        "source": KPI_CSV.name,
    }