import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "saas.db"
SQL_PATH = ROOT / "sql" / "segment_monthly_revenue.sql"


def main():
    if not DB_PATH.exists():
        raise SystemExit("saas.db not found. Run load_to_sqlite.py first.")
    sql = SQL_PATH.read_text(encoding="utf-8")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(sql).fetchall()
    finally:
        conn.close()

    if not rows:
        print("No rows returned")
        return

    headers = rows[0].keys()
    print(" | ".join(headers))
    print("-" * 60)
    for row in rows:
        print(" | ".join(str(row[h]) for h in headers))


if __name__ == "__main__":
    main()
