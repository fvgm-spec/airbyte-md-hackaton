WITH customer_accounts AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        COUNT(DISTINCT a.account_id) as total_accounts,
        SUM(CASE WHEN a.account_type = 'Investment' THEN 1 ELSE 0 END) as investment_accounts
    FROM {{ source('main', 'customerss3') }} c
    LEFT JOIN {{ source('main', 'accountss3') }} a ON c.customer_id = a.customer_id
    GROUP BY 1,2
)
SELECT * FROM customer_accounts