---
title: Financial Data Lake Integration Pipeline S3 to MotherDuck ETL
---

<Details title='Project description'>

  An automated data integration pipeline that extracts financial data (accounts, customers, investments, and transactions) from date-partitioned CSV files in Amazon S3 and loads them into corresponding tables in MotherDuck warehouse. This pipeline uses Airbyte Cloud to handle the ETL process, enabling real-time synchronization of financial data while maintaining data integrity and proper table relationships through a well-structured schema design. The system supports incremental updates and historical data tracking, making it ideal for financial reporting and analysis.
</Details>

<Details title='Customer Demographics Analysis'>

  This query provides key demographic statistics about customer ages, useful for understanding customer base distribution.
</Details>

```sql customer_demographics_analysis
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
FROM motherduck.customers;
```

<Details title='Risk Profile Distribution'>

  This analysis shows how risk profiles correlate with customer demographics and investment behavior.
</Details>

```sql risk_profile_analysis
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

<BarChart 
    data={risk_profile_analysis} 
    x="risk_profile" 
    y="avg_investment_amount"
    title="Avg Investment Amount by Risk Profile"
/>

<ScatterPlot  
    data={risk_profile_analysis} 
    x="avg_credit_score" 
    y="avg_investment_amount"
    title="Risk Profile: Credit Score vs Investment Amount"
/>

```sql customer_demographics 
SELECT 
    CASE 
        WHEN CAST(customer_age AS INTEGER) < 30 THEN 'Under 30'
        WHEN CAST(customer_age AS INTEGER) BETWEEN 30 AND 50 THEN '30-50'
        ELSE 'Over 50'
    END as age_group,
    COUNT(*) as customer_count,
    ROUND(AVG(CAST(credit_score AS DOUBLE)), 2) as avg_credit_score,
    ROUND(AVG(CAST(annual_income AS DOUBLE)), 2) as avg_annual_income
FROM motherduck.customers
GROUP BY age_group
ORDER BY age_group;
```

<BarChart 
    data={customer_demographics}
    x="age_group"
    y={["avg_credit_score", "avg_annual_income"]}
    title="Age Group Financial Metrics"
/>


<Details title='Investment Portfolio Analysis'>

  This query provides a comprehensive view of investment distribution across different sectors and investment types.
</Details>

```sql investment_portfolio_analysis
WITH portfolio_stats AS (
    SELECT 
        i.market_sector,
        i.investment_type,
        COUNT(*) as investment_count,
        ROUND(AVG(i.investment_amount::DOUBLE), 2) as avg_amount,
        ROUND(AVG(i.interest_rate::DOUBLE), 2) as avg_interest_rate,
        ROUND(SUM(i.investment_amount::DOUBLE), 2) as total_investment
    FROM motherduck.investments i
    GROUP BY i.market_sector, i.investment_type
)
SELECT 
    market_sector,
    investment_type,
    investment_count,
    avg_amount,
    avg_interest_rate,
    total_investment,
    ROUND(100.0 * total_investment / SUM(total_investment) OVER (), 2) as portfolio_percentage
FROM portfolio_stats
ORDER BY total_investment DESC;
```

<BarChart
    data={investment_portfolio_analysis}
    x="market_sector"
    y="avg_interest_rate"
    series="investment_type"
    title="Average Interest Rates by Sector"
/>

<DataTable 
    data={investment_portfolio_analysis}
    search=true
    pagination=true
/>


```sql transactions_pattern_over_time
SELECT 
    DATE_TRUNC('month', transaction_date::DATE) as month,
    transaction_type,
    COUNT(*) as transaction_count,
    COUNT(DISTINCT account_id) as unique_accounts,
    ROUND(AVG(transaction_amount::DOUBLE), 2) as avg_amount,
    ROUND(SUM(transaction_amount::DOUBLE), 2) as total_amount
    --ROUND(AVG(CAST(transaction_amount AS DOUBLE)), 2) as avg_amount,
    --ROUND(SUM(CAST(transaction_amount AS DOUBLE)), 2) as total_amount
FROM motherduck.transactions
GROUP BY 1, 2
ORDER BY month DESC, transaction_count DESC;
```

```sql high_value_customer_insights
WITH customer_metrics AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.credit_score,
        COUNT(DISTINCT a.account_id) as account_count,
        COUNT(DISTINCT t.transaction_id) as transaction_count,
        ROUND(SUM(t.transaction_amount::DOUBLE), 2) as total_transaction_volume,
        COUNT(DISTINCT i.investment_id) as investment_count,
        ROUND(SUM(i.investment_amount::DOUBLE), 2) as total_investments
    FROM motherduck.customers c
    LEFT JOIN motherduck.accounts a ON c.customer_id = a.customer_id
    LEFT JOIN motherduck.transactions t ON a.account_id = t.account_id
    LEFT JOIN motherduck.investments i ON a.account_id = i.account_id
    GROUP BY c.customer_id, c.customer_name, c.credit_score
)
SELECT 
    customer_name,
    credit_score,
    account_count,
    transaction_count,
    total_transaction_volume,
    investment_count,
    total_investments,
    ROUND(total_investments + total_transaction_volume, 2) as total_value
FROM customer_metrics
WHERE (total_investments + total_transaction_volume) > 0
ORDER BY total_value DESC
LIMIT 100;
```
