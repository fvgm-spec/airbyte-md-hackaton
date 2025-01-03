## Complete ETL pipeline using Airbyte Mother Duck connector

### The Dataset

The dataset used for this project is a synthetic one generated using the versatile Python [Faker](https://pypi.org/project/Faker/) module, it basically sets a `FinancialProvider` class to generate multiple *investment_types*, *transaction_types* and *risk_profiles* for further analysis by the end users in the UI that will be implemented using [Evidence](https://evidence.dev/). 

Bellow is a sample of the [data_generator.py](https://github.com/fvgm-spec/airbyte-md-hackaton/blob/main/data_generator.py) script that generates synthetic financial datasets. The generator creates interconnected CSV files containing `customers` information, `accounts`, `transactions`, and `investments`.:

<p>
<div class="column">
    <img src="./img/faker.png" style="height: 12rem"/>
  </div>
</p>

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

I wanted to create a standalone workflow that generate each a of datasets required for the project in a daily basis, so GitHub Actions is ideal for this purpose, it can be set as an automated system that can run in a cron based schedule, and finally store the generated daily data in AWS S3.

<p>
<div class="column">
    <img src="./img/github_actions.png" style="height: 16rem"/>
  </div>
</p>

#### System Overview

* Daily generation of financial datasets (customers, accounts, transactions, investments)
* Random variation in data volume
* Automatic upload to AWS S3
* Manual trigger option via `workflow_dispatch`


#### Features

* Monitoring/Maintenance: Built-in logging, execution history, error notifications, easy workflow modifications via email.

* Infrastructure Benefits: Free for public repositories, no need for dedicated servers, built-in secret management.

* Automation: Scheduled execution `(cron: '0 0 * * *')`, manual triggers via `workflow_dispatch`, environment setup automation, dependency management.

#### Synthetic data genaration action

In the case of this project the [workflow](https://github.com/fvgm-spec/airbyte-md-hackaton/blob/main/.github/workflows/daily_data_generation.yml#L33) performs the installation of basic dependencies on every run, then exewcutes the `data_generator.py` script directly from the GitHub repo, and as a last step, automatically stores te daily genarated data in a previously specified S3 bucket, that will be consumed by Airbyte during the Data Integration process.

```yaml
...
    - name: Generate Financial Dataset
      env:
        NUM_CUSTOMERS: ${{ steps.random.outputs.customers }}
        NUM_TRANSACTIONS: ${{ steps.random.outputs.transactions }}
      run: |
        mkdir -p generated_data
        python data_generator.py \
          --num_customers $NUM_CUSTOMERS \
          --num_transactions $NUM_TRANSACTIONS \
          --output_data generated_data
    
    - name: Configure AWS Credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Upload to S3
      run: |
        for file in generated_data/*/*.csv; do
          aws s3 cp "$file" "s3://${{ secrets.S3_BUCKET_NAME }}/financial_data/$(basename $(dirname $file))/$(basename $file)"
        done
```

### Airbyte Data Integration

Once the data extraction backend infrastructure was implemented, it's time to set the Airbyte connections. It basically sets 4 data streams for each of the datasets stored in the S3 bucket:

![s3_data](./img/s3_data.png)

Each single stream syncs the data using the Aibyte S3 source connector from the S3 bucket according to the search pattern `financial-data1215/financial_data/YYYY-MM-DD/`, this way all folders identified with the corresponding date by each folder will be integrated from the `customers`, `accounts`, `transactions`, and `investments` CSV files to be replicated to MotherDuck destination:

![s3_source](./img/s3_source.png)

For the MotherDuck Airbyte connector, there are 4 active connections corresponding to each of the 4 financial datasets: 

![airbyte_connections](./img/airbyte_connections.png)

The search pattern set in the MotherDuck connector settings in Airbyte compiles all the CSV files in a single stream to be dumped in a database table in MotherDuck Warehouse.

### The Data Warehouse

<p>
<div class="column">
    <img src="./img/md.jpeg" style="height: 13rem"/>
  </div>
</p>

As defined in [MotherDuck Website](https://motherduck.com/docs/concepts/data-warehousing/):

> MotherDuck is a cloud-native data warehouse, built on top of DuckDB, a fast in-process analytical database. It inherits some features from DuckDB that present opportunities to think differently about data warehousing methods in order to achieve high levels of performance and simplify the experience.


Motherduck UI is very flexible to work with multiple data sources and users in a colaborative way. In the image above I have already executed the data integration process from the S3 data generated by the [GitHub Actions process](https://github.com/fvgm-spec/airbyte-md-hackaton/blob/main/.github/workflows/daily_data_generation.yml), tables represented by the purple arrows:

* customerss3
* accountss3
* transactionss3
* investmentss3


I also created some [dbt models](https://github.com/fvgm-spec/airbyte-md-hackaton/tree/main/financial_dw) that generated some addittional tables in the MotherDuck Warehouse, tables represented by the red arrows:

* customer_profile
* investment_analysis

![md_ui](./img/md-ui.png)


### The UI

<p>
<div class="column">
    <img src="./img/evidence.png" style="height: 16rem"/>
  </div>
</p>

The UI where the users will be able to interact with the data is developed using the open-source BI tool Evidence
