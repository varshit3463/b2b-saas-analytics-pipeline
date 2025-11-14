import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
random.seed(42)

REGIONS = ["NA", "EMEA", "APAC", "LATAM"]
INDUSTRIES = ["Fintech", "Healthcare", "Retail", "Manufacturing", "Media"]
PLANS = {
    "Starter": 400,
    "Growth": 1500,
    "Enterprise": 4500,
}
ROLES = ["admin", "manager", "analyst", "engineer"]
FEATURES = [
    "dashboards",
    "automation",
    "reporting",
    "api",
    "collaboration",
]

NUM_ACCOUNTS = 120
MONTHS_OF_HISTORY = 6


def random_date_within(days: int) -> datetime:
    return datetime.now() - timedelta(days=random.randint(0, days))


def generate_accounts():
    accounts = []
    for account_id in range(1, NUM_ACCOUNTS + 1):
        plan = random.choices(list(PLANS.keys()), weights=[0.4, 0.4, 0.2])[0]
        mrr = PLANS[plan]
        acv = mrr * 12 + random.randint(-500, 500)
        signup_date = random_date_within(900)
        accounts.append(
            {
                "account_id": account_id,
                "name": f"Account {account_id:03d}",
                "industry": random.choice(INDUSTRIES),
                "plan": plan,
                "acv": acv,
                "signup_date": signup_date.strftime("%Y-%m-%d"),
                "region": random.choice(REGIONS),
            }
        )
    return accounts


def generate_users(accounts):
    users = []
    user_id = 1
    for account in accounts:
        plan = account["plan"]
        seats = {
            "Starter": random.randint(5, 15),
            "Growth": random.randint(15, 40),
            "Enterprise": random.randint(40, 80),
        }[plan]
        admin_ids = random.sample(range(seats), k=max(1, seats // 10))
        for idx in range(seats):
            role = random.choice(ROLES)
            users.append(
                {
                    "user_id": user_id,
                    "account_id": account["account_id"],
                    "role": role,
                    "is_admin": "1" if idx in admin_ids else "0",
                    "last_active": random_date_within(60).strftime("%Y-%m-%d"),
                }
            )
            user_id += 1
    return users


def generate_subscriptions(accounts):
    subscriptions = []
    subscription_id = 1
    today = datetime.now().date().replace(day=1)
    for account in accounts:
        mrr = PLANS[account["plan"]]
        active = True
        for month_offset in range(MONTHS_OF_HISTORY, 0, -1):
            start = (today - timedelta(days=30 * month_offset))
            end = start + timedelta(days=29)
            status = "active" if active else "cancelled"
            if active and random.random() < 0.08:
                status = "cancelled"
                active = False
            subscriptions.append(
                {
                    "subscription_id": subscription_id,
                    "account_id": account["account_id"],
                    "period_start": start.strftime("%Y-%m-%d"),
                    "period_end": end.strftime("%Y-%m-%d"),
                    "status": status,
                    "mrr": mrr,
                }
            )
            subscription_id += 1
    return subscriptions


def generate_invoices(subscriptions):
    invoices = []
    for sub in subscriptions:
        amount = sub["mrr"]
        issued_date = datetime.strptime(sub["period_end"], "%Y-%m-%d") + timedelta(days=1)
        status = "paid" if sub["status"] == "active" or random.random() > 0.3 else "overdue"
        invoices.append(
            {
                "invoice_id": len(invoices) + 1,
                "subscription_id": sub["subscription_id"],
                "issued_date": issued_date.strftime("%Y-%m-%d"),
                "amount": amount,
                "currency": "USD",
                "payment_status": status,
            }
        )
    return invoices


def generate_feature_events(users):
    events = []
    event_id = 1
    for user in users:
        sessions = random.randint(3, 12)
        for _ in range(sessions):
            feature = random.choice(FEATURES)
            usage_date = random_date_within(90)
            events.append(
                {
                    "event_id": event_id,
                    "user_id": user["user_id"],
                    "feature": feature,
                    "usage_date": usage_date.strftime("%Y-%m-%d"),
                    "events_count": random.randint(1, 25),
                }
            )
            event_id += 1
    return events


def write_csv(filename, rows, headers):
    DATA_DIR.mkdir(exist_ok=True)
    path = DATA_DIR / filename
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    return path


def main():
    accounts = generate_accounts()
    users = generate_users(accounts)
    subscriptions = generate_subscriptions(accounts)
    invoices = generate_invoices(subscriptions)
    feature_events = generate_feature_events(users)

    file_map = {
        "accounts.csv": (accounts, accounts[0].keys()),
        "users.csv": (users, users[0].keys()),
        "subscriptions.csv": (subscriptions, subscriptions[0].keys()),
        "invoices.csv": (invoices, invoices[0].keys()),
        "feature_events.csv": (feature_events, feature_events[0].keys()),
    }

    for filename, (rows, headers) in file_map.items():
        write_csv(filename, rows, headers)
        print(f"Wrote {filename} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
