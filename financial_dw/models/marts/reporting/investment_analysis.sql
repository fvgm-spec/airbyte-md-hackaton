WITH investment_metrics AS (
    SELECT 
        a.customer_id,
        i.market_sector,
        COUNT(*) as investments_count,
        --SUM(i.investment_amount) as total_invested,
        SUM(CAST(i.investment_amount AS DOUBLE)) AS total_invested,
        AVG(CAST(i.return_percentage AS DOUBLE)) as avg_return
    FROM {{ source('main', 'investmentss3') }} i
    JOIN {{ source('main', 'accountss3') }} a ON i.account_id = a.account_id
    GROUP BY 1, 2
)
SELECT * FROM investment_metrics