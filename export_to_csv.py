import psycopg2
import pandas as pd

DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "monitoring_db",
    "user": "postgres",
    "password": "1234"
}

conn = psycopg2.connect(**DB)

raw_df = pd.read_sql("SELECT * FROM raw_events ORDER BY event_ts DESC;", conn)
raw_df.to_csv("raw_events.csv", index=False)

kpi_df = pd.read_sql("SELECT * FROM kpi_metrics_5min ORDER BY window_start DESC;", conn)
kpi_df.to_csv("kpi_metrics_5min.csv", index=False)

conn.close()
print("✅ CSV export completed: raw_events.csv, kpi_metrics_5min.csv")
