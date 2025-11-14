import csv
import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DB_PATH = DATA_DIR / "saas.db"

TABLE_DDL = {
    "accounts": """
        CREATE TABLE IF NOT EXISTS accounts (
            account_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            industry TEXT NOT NULL,
            plan TEXT NOT NULL,
            acv INTEGER NOT NULL,
            signup_date TEXT NOT NULL,
            region TEXT NOT NULL
        )
    """,
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            account_id INTEGER NOT NULL REFERENCES accounts(account_id),
            role TEXT NOT NULL,
            is_admin INTEGER NOT NULL,
            last_active TEXT NOT NULL
        )
    """,
    "subscriptions": """
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id INTEGER PRIMARY KEY,
            account_id INTEGER NOT NULL REFERENCES accounts(account_id),
            period_start TEXT NOT NULL,
            period_end TEXT NOT NULL,
            status TEXT NOT NULL,
            mrr REAL NOT NULL
        )
    """,
    "invoices": """
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id INTEGER PRIMARY KEY,
            subscription_id INTEGER NOT NULL REFERENCES subscriptions(subscription_id),
            issued_date TEXT NOT NULL,
            amount REAL NOT NULL,
            currency TEXT NOT NULL,
            payment_status TEXT NOT NULL
        )
    """,
    "feature_events": """
        CREATE TABLE IF NOT EXISTS feature_events (
            event_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(user_id),
            feature TEXT NOT NULL,
            usage_date TEXT NOT NULL,
            events_count INTEGER NOT NULL
        )
    """,
}


def reset_tables(conn):
    cursor = conn.cursor()
    for table in reversed(list(TABLE_DDL.keys())):
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    conn.commit()
    for ddl in TABLE_DDL.values():
        cursor.execute(ddl)
    conn.commit()


def load_csv(conn, table):
    csv_path = DATA_DIR / f"{table}.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing {csv_path}. Run generate_data.py first.")

    with csv_path.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = [tuple(row[col] for col in reader.fieldnames) for row in reader]

    placeholders = ",".join(["?"] * len(reader.fieldnames))
    columns = ",".join(reader.fieldnames)
    conn.executemany(
        f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
        rows,
    )
    conn.commit()
    print(f"Inserted {len(rows)} rows into {table}")


def main():
    DATA_DIR.mkdir(exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)
    try:
        reset_tables(conn)
        for table in TABLE_DDL.keys():
            load_csv(conn, table)
    finally:
        conn.close()
    print(f"Database ready at {DB_PATH}")


if __name__ == "__main__":
    main()
