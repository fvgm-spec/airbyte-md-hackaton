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

#### MotherDuck Data Warehouse instance

-- Run this snippet to attach database
ATTACH 'md:_share/my_db/800e02df-e793-452e-b6f7-8df2dc1df3ee';


### The UI

<p>
<div class="column">
    <img src="./img/evidence.png" style="height: 16rem"/>
  </div>
</p>

### Financial Data Lake Integration Pipeline

#### Project Overview

This project implements an end-to-end data pipeline that combines Airbyte connectors (S3 and MotherDuck) with Evidence for financial data visualization. The pipeline extracts financial data from S3, loads it into MotherDuck, and presents insights through an Evidence dashboard.

#### Architecture

<p>
<div class="column">
    <img src="./img/architecture.png" style="height: 30rem"/>
  </div>
</p>

#### Components

1. Data Source: Amazon S3 buckets containing partitioned CSV files with:

* Customer data
* Account information
* Transaction records
* Investment details


2. ETL Pipeline:

* Airbyte S3 source connector for data extraction
* Airbyte MotherDuck destination connector for data loading
* Automated synchronization with incremental updates

3. Data Warehouse:

* customerss3
* accountss3
* transactionss3
* investmentss3

4. Visualization Layer:

* Evidence project for creating interactive financial reports
* Custom SQL queries for data analysis
* Interactive dashboards and visualizations

#### Getting Started and Prerequisites

* Node.js (v14 or higher)
* npm or yarn
* MotherDuck account and connection details
* Evidence CLI

#### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd evidence_project
```

2. Install dependencies:

```bash
npm install
```

3. Configure MotherDuck connection:

```yaml
# connection.yaml
motherduck:
  token: your_motherduck_token
  database: your_database_name
```

4. Start the Evidence development server:

```bash
npm run dev
```

5. Access the dashboard:

Open your browser and navigate to http://localhost:3000

#### Available Reports

1. Risk Profile Analysis

* Customer distribution by risk level
* Average investment amounts
* Credit score correlations

2. Customer Demographics

* Age group distribution
* Financial behavior patterns
* Credit score analysis

3. Investment Portfolio

* Market sector distribution
* Investment type breakdown
* Interest rate analysis

4. Transaction Trends

* Monthly transaction volumes
* Transaction type patterns
* Currency distribution

#### How the application works?

> In this first video you will see how the pipeline is done from the beginning (GitHub repo), then how the Python scripts are triggered (GitHub Actions). You will also learn how the pipeline continues working in Airbyte, how the sources and destinations are configured, and then in MotherDuck Data Warehouse, how can the resulting tables be queried. 

Check that out in this first video >> [How the pipeline works?](https://youtu.be/BlTTMvABxoo)

> In this second video shows how are the evidence settings done, and also how the sources are configured. Lastly it will show how keep the Evidence project up and running, it will only take a few minutes.

Evdence project up and running... >> [Run your Evidence project](https://youtu.be/84XlCzqpKi0)

> In his last video you will finally see how the magic happens >> [Start Evidence project](https://youtu.be/-166gwMvyvs)

Enjoy and keep on Airbyte...

<p>
<div class="column">
    <img src="./img/airbyte2.png" style="height: 13rem"/>
  </div>
</p>

