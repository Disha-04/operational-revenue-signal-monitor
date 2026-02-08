from datetime import datetime, timedelta, timezone
import psycopg2

DB = {
    "host": "127.0.0.1",
    "port": 5432,
    "dbname": "monitoring_db",
    "user": "postgres",
    "password": "1234"
}

LATENCY_SLA_MS = 1200   # SLA threshold
FAIL_RATE_WARN = 0.30  # 30%
FRESHNESS_CRIT_MIN = 10

def main():
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    window_end = datetime.now(timezone.utc)
    window_start = window_end - timedelta(minutes=5)

    # Core KPIs
    cur.execute("""
        SELECT
            COUNT(*) AS events_count,
            COUNT(*) FILTER (WHERE event_type = 'purchase') AS purchases_count,
            COALESCE(SUM(amount) FILTER (WHERE event_type = 'purchase'), 0) AS revenue,
            COUNT(*) FILTER (WHERE event_type = 'payment_failed')::float
              / NULLIF(COUNT(*) FILTER (WHERE event_type IN ('purchase','payment_failed')),0)
              AS payment_fail_rate,
            AVG(latency_ms)::int AS avg_latency_ms,
            PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms)::int AS p95_latency_ms
        FROM raw_events
        WHERE event_ts >= %s AND event_ts < %s
          AND latency_ms IS NOT NULL
    """, (window_start, window_end))

    (
        events_count,
        purchases_count,
        revenue,
        payment_fail_rate,
        avg_latency_ms,
        p95_latency_ms
    ) = cur.fetchone()

    payment_fail_rate = payment_fail_rate or 0.0
    avg_latency_ms = avg_latency_ms or 0
    p95_latency_ms = p95_latency_ms or 0

    # Active users (30 min)
    cur.execute("""
        SELECT COUNT(DISTINCT user_id)
        FROM raw_events
        WHERE event_ts >= %s
    """, (window_end - timedelta(minutes=30),))
    active_users_30m = cur.fetchone()[0]

    # Data freshness
    cur.execute("SELECT MAX(event_ts) FROM raw_events")
    last_event_ts = cur.fetchone()[0]
    freshness_minutes = int((window_end - last_event_ts).total_seconds() / 60)

    # Alert logic
    alert_flag = "OK"
    sla_breach_flag = False
    alert_reason = "All metrics within SLA"

    if freshness_minutes > FRESHNESS_CRIT_MIN:
        alert_flag = "CRIT"
        sla_breach_flag = True
        alert_reason = "CRIT: Data freshness exceeded 10 minutes"

    elif p95_latency_ms > LATENCY_SLA_MS:
        alert_flag = "WARN"
        sla_breach_flag = True
        alert_reason = f"WARN: p95 latency {p95_latency_ms}ms exceeded SLA"

    elif payment_fail_rate > FAIL_RATE_WARN:
        alert_flag = "WARN"
        alert_reason = f"WARN: Payment failure rate {payment_fail_rate:.2%}"

    # Insert KPI row
    cur.execute("""
        INSERT INTO kpi_metrics_5min (
            window_start, window_end,
            events_count, purchases_count,
            revenue, payment_fail_rate,
            active_users_30m,
            data_freshness_minutes,
            alert_flag,
            avg_latency_ms,
            p95_latency_ms,
            sla_breach_flag,
            alert_reason
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (window_start, window_end) DO NOTHING
    """, (
        window_start, window_end,
        events_count, purchases_count,
        revenue, payment_fail_rate,
        active_users_30m,
        freshness_minutes,
        alert_flag,
        avg_latency_ms,
        p95_latency_ms,
        sla_breach_flag,
        alert_reason
    ))

    conn.commit()
    print("KPI computed:", alert_flag, "|", alert_reason)

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()