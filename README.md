## Complete ETL pipeline using Airbyte Mother Duck connector

### Financial Data Generator

A Python script that generates realistic financial datasets for testing and development purposes. The generator creates interconnected CSV files containing `customers` information, `accounts`, `transactions`, and `investments`.

#### Features

- Generates four related datasets:
  - Customers (demographics, income, credit score)
  - Accounts (types, risk profiles)
  - Transactions (deposits, withdrawals, purchases)
  - Investments (types, amounts, sectors)
- Creates UUID-based relationships between tables
- Uses realistic fake data for names, emails, and locations
- Organizes output in date-based directory structure

#### Installation

```bash
pip install faker pandas
```

#### Usage

```bash
python generator.py --num_customers 100 --num_transactions 200 --output_data generated_data
```

#### Arguments

- `--num_customers`: Number of customers to generate (default: 100)
- `--num_transactions`: Number of transactions to generate (default: 200)
- `--output_data`: Directory to save generated CSV files (default: 'generated_data')

#### Output Structure

```
generated_data/
└── YYYY-MM-DD/
    ├── customers.csv
    ├── accounts.csv
    ├── transactions.csv
    └── investments.csv
```

#### Data Schema

**customers.csv**

- customer_id (UUID)
- customer_name
- customer_email
- customer_age (18-75)
- annual_income ($20k-$500k)
- credit_score (300-850)
- country
- city

**accounts.csv**

- account_id (UUID)
- customer_id (UUID)
- account_type
- risk_profile
- opening_date

### Resources
* [MotherDuck Official site](https://motherduck.com/docs/getting-started/)
* [MotherDuck Airbyte connector](https://docs.airbyte.com/integrations/destinations/motherduck)
* [GitHub repo](https://github.com/airbytehq/airbyte/tree/master/airbyte-integrations/connectors/destination-motherduck)