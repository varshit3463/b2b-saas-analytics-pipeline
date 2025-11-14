WITH paid_invoices AS (
    SELECT
        s.account_id,
        DATE(substr(i.issued_date, 1, 7) || "-01") AS invoice_month,
        i.amount
    FROM invoices i
    JOIN subscriptions s ON s.subscription_id = i.subscription_id
    WHERE i.payment_status = "paid"
),
revenue_by_industry AS (
    SELECT
        a.industry,
        pi.invoice_month,
        COUNT(DISTINCT pi.account_id) AS paying_accounts,
        SUM(pi.amount) AS collected_arr
    FROM paid_invoices pi
    JOIN accounts a ON a.account_id = pi.account_id
    GROUP BY a.industry, pi.invoice_month
),
feature_by_industry AS (
    SELECT
        a.industry,
        DATE(substr(fe.usage_date, 1, 7) || "-01") AS usage_month,
        SUM(fe.events_count) AS total_events,
        COUNT(DISTINCT fe.user_id) AS active_users
    FROM feature_events fe
    JOIN users u ON u.user_id = fe.user_id
    JOIN accounts a ON a.account_id = u.account_id
    GROUP BY a.industry, usage_month
),
calendar AS (
    SELECT industry, invoice_month AS month FROM revenue_by_industry
    UNION
    SELECT industry, usage_month AS month FROM feature_by_industry
)
SELECT
    c.industry,
    c.month,
    COALESCE(r.paying_accounts, 0) AS paying_accounts,
    COALESCE(ROUND(r.collected_arr, 2), 0) AS collected_arr,
    COALESCE(ROUND(f.total_events, 2), 0) AS total_feature_events,
    COALESCE(f.active_users, 0) AS active_users
FROM calendar c
LEFT JOIN revenue_by_industry r
    ON r.industry = c.industry AND r.invoice_month = c.month
LEFT JOIN feature_by_industry f
    ON f.industry = c.industry AND f.usage_month = c.month
ORDER BY c.month, c.industry;
