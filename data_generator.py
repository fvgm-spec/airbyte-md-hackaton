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

def generate_datasets(num_customers: int, num_transactions: int, output_data: str):
    """
    Generate a relational financial dataset with multiple interconnected tables.
    
    Args:
        num_customers (int): Number of customers to generate
        num_transactions (int): Number of transactions to generate
        output_data (str): Directory to save generated CSV files
    """
    # Create date-based directory structure
    today = date.today().strftime("%Y-%m-%d")
    output_dir = os.path.join(output_data, today)
    os.makedirs(output_dir, exist_ok=True)
    
    fake = faker.Faker()
    fake.add_provider(FinancialProvider)
    
    # Customer Table
    customers = []
    customer_ids = []
    for _ in range(num_customers):
        customer_id = str(uuid.uuid4())
        customer_ids.append(customer_id)
        
        customer = {
            'customer_id': customer_id,
            'customer_name': fake.name(),
            'customer_email': fake.email(),
            'customer_age': random.randint(18, 75),
            'annual_income': round(random.uniform(20000, 500000), 2),
            'credit_score': random.randint(300, 850),
            'country': fake.country_code(),
            'city': fake.city()
        }
        customers.append(customer)
    
    # Account Table
    accounts = []
    account_ids = []
    for customer_id in customer_ids:
        num_accounts = random.randint(1, 3)
        for _ in range(num_accounts):
            account_id = str(uuid.uuid4())
            account_ids.append(account_id)
            
            account = {
                'account_id': account_id,
                'customer_id': customer_id,
                'account_type': random.choice([
                    'Checking', 'Savings', 'Investment', 
                    'Retirement', 'Business', 'Joint'
                ]),
                'risk_profile': fake.risk_profile(),
                'opening_date': fake.date_between(start_date='-5y', end_date='today')
            }
            accounts.append(account)
    
    # Transactions Table
    transactions = []
    for _ in range(num_transactions):
        account_id = random.choice(account_ids)
        
        transaction = {
            'transaction_id': str(uuid.uuid4()),
            'account_id': account_id,
            'transaction_type': fake.transaction_type(),
            'transaction_amount': round(random.uniform(10, 10000), 2),
            'currency': fake.currency_code(),
            'transaction_date': fake.date_between(start_date='-2y', end_date='today')
        }
        transactions.append(transaction)
    
    # Investment Table
    investments = []
    for account_id in account_ids:
        num_investments = random.randint(0, 3)
        for _ in range(num_investments):
            investment = {
                'investment_id': str(uuid.uuid4()),
                'account_id': account_id,
                'investment_type': fake.investment_type(),
                'investment_amount': round(random.uniform(100, 50000), 2),
                'market_sector': random.choice([
                    'Technology', 'Finance', 'Healthcare', 
                    'Energy', 'Retail', 'Manufacturing'
                ]),
                'interest_rate': round(random.uniform(0.5, 15.0), 2),
                'return_percentage': round(random.uniform(-10, 20), 2)
            }
            investments.append(investment)
    
    # Save files with simplified names in date-based directory
    pd.DataFrame(customers).to_csv(os.path.join(output_dir, 'customers.csv'), index=False)
    pd.DataFrame(accounts).to_csv(os.path.join(output_dir, 'accounts.csv'), index=False)
    pd.DataFrame(transactions).to_csv(os.path.join(output_dir, 'transactions.csv'), index=False)
    pd.DataFrame(investments).to_csv(os.path.join(output_dir, 'investments.csv'), index=False)
    
    return None

def main():
    parser = argparse.ArgumentParser(description='Generate Financial Dataset')
    parser.add_argument('--num_customers', type=int, default=100, 
                        help='Number of customers to generate')
    parser.add_argument('--num_transactions', type=int, default=200, 
                        help='Number of transactions to generate')
    parser.add_argument('--output_data', type=str, default='generated_data', 
                        help='Directory to save generated CSV files')
    
    args = parser.parse_args()
    
    generate_datasets(
        num_customers=args.num_customers, 
        num_transactions=args.num_transactions, 
        output_data=args.output_data
    )

if __name__ == '__main__':
    main()
