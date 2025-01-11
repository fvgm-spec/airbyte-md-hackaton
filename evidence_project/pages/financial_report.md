---
title: Financial Report
---

<Details title='How to edit this page'>

  This page can be found in your project at `/pages/financial_report.md`. Make a change to the markdown file and save it to see the change take effect in your browser.
</Details>

```sql CUSTOMERS_BY_AGE
  SELECT
      'Summary Stats' as statistic,
      COUNT(*) as count,
      ROUND(AVG(customer_age::DOUBLE), 2) as age_mean,
      ROUND(STDDEV(customer_age::DOUBLE), 2) as age_std,
      MIN(customer_age::DOUBLE) as age_min,
      ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY customer_age::DOUBLE), 2) as age_25,
      ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY customer_age::DOUBLE), 2) as age_50,
      ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY customer_age::DOUBLE), 2) as age_75,
      MAX(customer_age) as age_max
FROM motherduck.customers
```

``` sql RISK_PROFILE_DISTRIBUTION
SELECT 
    a.risk_profile,
    COUNT(DISTINCT a.customer_id) as customer_count,
    ROUND(AVG(c.customer_age::DOUBLE), 2) as avg_age,
    ROUND(AVG(c.credit_score::DOUBLE), 2) as avg_credit_score,
    COUNT(DISTINCT i.investment_id) as investment_count,
    ROUND(AVG(i.investment_amount::DOUBLE), 2) as avg_investment_amount
FROM motherduck.accounts a
LEFT JOIN motherduck.customers c ON a.customer_id = c.customer_id
LEFT JOIN motherduck.investments i ON a.account_id = i.account_id
GROUP BY a.risk_profile
ORDER BY customer_count DESC;
```

``` sql test
SELECT
    a.risk_profile, count(*)
FROM motherduck.accounts a
GROUP BY a.risk_profile
;
```