-- sql/build_features.sql  (Nubank-style mapping)
CREATE OR REPLACE VIEW v_features AS
SELECT
  ROW_NUMBER() OVER () AS id,
  CAST(issue_date AS TIMESTAMP)                                   AS issue_date,
  target_default                                                  AS target,
  credit_limit_brl * utilization_ratio                            AS loan_amount,
  total_payment_brl                                               AS total_payment,
  interest_rate                                                   AS interest_rate,
  dti_pct                                                         AS dti,
  DATE_TRUNC('month', CAST(issue_date AS TIMESTAMP))              AS issue_month,
  EXTRACT(year FROM CAST(issue_date AS TIMESTAMP))                AS issue_year,
  EXTRACT(month FROM CAST(issue_date AS TIMESTAMP))               AS issue_month_num,
  CASE WHEN monthly_income_brl > 0 THEN (credit_limit_brl * utilization_ratio) / monthly_income_brl ELSE NULL END AS loan_to_income,
  CASE WHEN credit_limit_brl > 0 THEN total_payment_brl / credit_limit_brl ELSE NULL END AS payment_to_limit,
  CAST(loan_status AS VARCHAR)                                     AS loan_status,
  CAST(application_channel AS VARCHAR)                             AS channel,
  age, state, education, employment, months_on_book, pix_txn_30d, delinq_30, delinq_60, delinq_90, credit_inquiries_6m
FROM bank_loan_data;
