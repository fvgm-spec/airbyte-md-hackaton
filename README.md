## Complete ETL pipeline using Airbyte Mother Duck connector

### The Dataset

The dataset used for this project is a synthetic one generated using the versatile Python [Faker](https://pypi.org/project/Faker/) module, it basically sets a `FinancialProvider` class to generate multiple *investment_types*, *transaction_types* and *risk_profiles* for further analysis by the end users in the UI that will be implemented using [Evidence](https://evidence.dev/). 

Bellow is a sample of the [data_generator.py](https://github.com/fvgm-spec/airbyte-md-hackaton/blob/main/data_generator.py) script that generates synthetic financial datasets. The generator creates interconnected CSV files containing `customers` information, `accounts`, `transactions`, and `investments`.:

```python
import faker
from faker.providers import BaseProvider
import pandas as pd
import random
import uuid
import argparse
import os
from datetime import date

class FinancialProvider(BaseProvider):
    def investment_type(self):
        """Generate a realistic investment type."""
        return random.choice([
            'Stocks', 'Bonds', 'Mutual Funds', 'ETFs', 
            'Cryptocurrency', 'Real Estate Investment Trust', 
            'Commodities', 'Government Bonds'
        ])
    
    def transaction_type(self):
        """Generate a transaction type."""
        return random.choice([
            'Deposit', 'Withdrawal', 'Transfer', 
            'Purchase', 'Sale', 'Dividend Reinvestment'
        ])
    
    def risk_profile(self):
        """Generate an investment risk profile."""
        return random.choice([
            'Low Risk', 'Medium Risk', 'High Risk', 
            'Aggressive', 'Conservative', 'Balanced'
        ])
```

#### Features

- The script generates 4 related datasets:
  - Customers (including demographics, income, credit score)
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

```bash
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


### The Workflow


### Airbyte Data Integration


### The Datawarehouse


### The UI


