---
title: Finantial Data Generator
---

<Details title='How to edit this page'>

  This page can be found in your project at `/pages/index.md`. Make a change to the markdown file and save it to see the change take effect in your browser.
</Details>

```sql customer_ages
  SELECT
    'Summary Stats' as statistic,
    COUNT(*) as count,
    
    -- customer_age statistics
    ROUND(AVG(customer_age::DOUBLE), 2) as age_mean,
    ROUND(STDDEV(customer_age::DOUBLE), 2) as age_std,
    MIN(customer_age::DOUBLE) as age_min,
    ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY customer_age::DOUBLE), 2) as age_25,
    ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY customer_age::DOUBLE), 2) as age_50,
    ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY customer_age::DOUBLE), 2) as age_75,
    MAX(customer_age) as age_max
FROM motherduck.customers;
```