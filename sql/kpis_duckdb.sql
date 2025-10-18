-- sql/kpis_duckdb.sql
CREATE OR REPLACE VIEW v_monthly_kpis AS
SELECT
  DATE_TRUNC('month', issue_date) AS month,
  COUNT(*)                        AS loan_applications,
  SUM(loan_amount)                AS total_funded_amount,
  SUM(total_payment)              AS amount_received,
  AVG(interest_rate)              AS avg_interest_rate,
  AVG(dti)                        AS avg_dti,
  AVG(target)                     AS default_rate
FROM v_features
GROUP BY 1
ORDER BY 1;

CREATE OR REPLACE VIEW v_good_bad AS
SELECT
  SUM(CASE WHEN target = 0 THEN 1 ELSE 0 END) AS good_loan_count,
  SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) AS bad_loan_count,
  SUM(CASE WHEN target = 0 THEN loan_amount ELSE 0 END)  AS good_funded,
  SUM(CASE WHEN target = 1 THEN loan_amount ELSE 0 END)  AS bad_funded,
  SUM(CASE WHEN target = 0 THEN total_payment ELSE 0 END)  AS good_received,
  SUM(CASE WHEN target = 1 THEN total_payment ELSE 0 END)  AS bad_received
FROM v_features;

CREATE OR REPLACE VIEW v_mom_received AS
WITH monthly AS (
  SELECT DATE_TRUNC('month', issue_date) AS month, SUM(total_payment) AS amount
  FROM v_features
  GROUP BY 1
)
SELECT
  month,
  amount AS current_month_amount,
  LAG(amount) OVER (ORDER BY month) AS previous_month_amount,
  amount - LAG(amount) OVER (ORDER BY month) AS mom_change
FROM monthly
ORDER BY month;
