# B2B SaaS Usage & Revenue Pipeline

This repo completes the Cursor A-SDLC exercise with a unique business-to-business SaaS twist: synthetic account data is generated, loaded into SQLite, and queried to blend revenue plus product usage signals.

## Overview
- **Data generation**: `scripts/generate_data.py` outputs five relational CSVs (`accounts`, `users`, `subscriptions`, `invoices`, `feature_events`) with coherent foreign keys and deterministic randomness for repeatable runs.
- **Ingestion**: `scripts/load_to_sqlite.py` rebuilds `data/saas.db`, creates normalized tables, and bulk-loads every CSV.
- **Analysis**: `scripts/run_analysis.py` executes `sql/segment_monthly_revenue.sql`, which joins revenue and feature-usage telemetry to report ARR and engagement by industry and month.

## Prerequisites
- Python 3.11+
- `sqlite3` CLI (optional for ad-hoc checks)

## Quick Start
1. (Optional) create/activate a virtualenv.
2. Generate data:
   ```
   python scripts/generate_data.py
   ```
3. Load data into SQLite:
   ```
   python scripts/load_to_sqlite.py
   ```
4. Run the analytics query:
   ```
   python scripts/run_analysis.py
   ```

Each command prints status (row counts or query output). You can re-run any time; outputs stay consistent because the generator seeds `random`.

## Files
- `data/`: generated CSVs plus `saas.db`.
- `scripts/`: automation helpers (generate, load, analyze).
- `sql/segment_monthly_revenue.sql`: industry-by-month insight mixing invoices, subscriptions, accounts, users, and feature events.

## Verification Tips
- After loading, try `sqlite3 data/saas.db "SELECT COUNT(*) FROM subscriptions;"` to sanity-check.
- Duplicate the SQL file to explore other SaaS questions (churn, seat utilization, etc.) and reuse `run_analysis.py` to print results.

## Next Steps
- Push to GitHub for submission.
- Extend the dataset or add dashboards/visualizations highlighting SaaS health metrics.
