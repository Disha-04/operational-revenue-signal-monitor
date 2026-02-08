import time, uuid, random
from datetime import datetime, timezone
import psycopg2

DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "monitoring_db",
    "user": "postgres",
    "password": "1234"  
}

EVENT_TYPES = ["login", "purchase", "payment_failed"]
GATEWAYS = ["Stripe", "Adyen", "PayPal", "VisaNet"]
FAIL_CODES = ["05", "51", "14", "91"]  # common decline-style codes


def connect():
    return psycopg2.connect(**DB)


def generate_event():
    event_type = random.choices(EVENT_TYPES, weights=[60, 30, 10])[0]

    amount = None
    status = "success"
    gateway_name = None
    response_code = None
    latency_ms = None
    retry_attempt = 0

    if event_type in ("purchase", "payment_failed"):
        amount = round(random.uniform(5, 250), 2)
        gateway_name = random.choice(GATEWAYS)
        latency_ms = random.randint(150, 1600)
        retry_attempt = random.choices([0, 1, 2], weights=[75, 20, 5])[0]

        if event_type == "purchase":
            status = "success"
            response_code = "00"
        else:
            status = "fail"
            response_code = random.choice(FAIL_CODES)

    return {
        "event_id": str(uuid.uuid4()),
        "event_ts": datetime.now(timezone.utc),
        "user_id": f"user_{random.randint(1, 2000)}",
        "event_type": event_type,
        "amount": amount,
        "status": status,
        "gateway_name": gateway_name,
        "response_code": response_code,
        "latency_ms": latency_ms,
        "retry_attempt": retry_attempt,
    }


def insert_event(conn, e):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO raw_events(
              event_id, event_ts, user_id, event_type, amount, status,
              gateway_name, response_code, latency_ms, retry_attempt
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (event_id) DO NOTHING
            """,
            (
                e["event_id"], e["event_ts"], e["user_id"], e["event_type"], e["amount"], e["status"],
                e["gateway_name"], e["response_code"], e["latency_ms"], e["retry_attempt"]
            )
        )
    conn.commit()


if __name__ == "__main__":
    conn = connect()
    print("Generating events... Ctrl+C to stop.")
    try:
        while True:
            batch = random.randint(10, 40)
            for _ in range(batch):
                insert_event(conn, generate_event())
            print(f"Inserted {batch} events at {datetime.utcnow().isoformat()}Z")
            time.sleep(60)
    except KeyboardInterrupt:
        print("Stopped.")
    finally:
        conn.close()