---
title: Financial Data Lake Integration Pipeline: S3 to MotherDuck ETL
---

<Details title='Project description'>

  An automated data integration pipeline that extracts financial data (accounts, customers, investments, and transactions) from date-partitioned CSV files in Amazon S3 and loads them into corresponding tables in MotherDuck warehouse. This pipeline uses Airbyte Cloud to handle the ETL process, enabling real-time synchronization of financial data while maintaining data integrity and proper table relationships through a well-structured schema design. The system supports incremental updates and historical data tracking, making it ideal for financial reporting and analysis.
</Details>