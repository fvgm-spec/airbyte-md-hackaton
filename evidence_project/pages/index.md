---
title: Financial Data Lake Integration Pipeline
---

<Details title='How this project works?'>
  An automated data integration pipeline that extracts financial data (accounts, customers, investments, and transactions) from date-partitioned CSV files in Amazon S3 and loads them into corresponding tables in MotherDuck warehouse. This pipeline uses Airbyte Cloud to handle the ETL process, enabling real-time synchronization of financial data while maintaining data integrity and proper table relationships through a well-structured schema design. The system supports incremental updates and historical data tracking, making it ideal for financial reporting and analysis.
</Details>

```sql accounts_types
  select
      account_type
  from motherduck.accounts
  group by account_type
```

