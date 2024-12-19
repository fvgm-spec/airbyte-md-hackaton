import boto3
import pandas as pd
from typing import Dict

def read_csv_from_s3(date: str, file_type: str) -> pd.DataFrame:
    """
    Read a specific CSV file from a date folder in S3
    
    Args:
        date (str): Date folder name (e.g., '2024-12-19')
        file_type (str): Type of file to read ('accounts', 'customers', 'investments', 'transactions')
    
    Returns:
        pd.DataFrame: DataFrame containing the CSV data
    """
    # S3 bucket name and base path from your structure
    bucket_name = 'financial-data1215'
    base_path = 'financial_data'
    
    # Construct the full path including the financial_data directory
    object_key = f"{base_path}/{date}/{file_type}.csv"
    
    print(f"Attempting to access: s3://{bucket_name}/{object_key}")  # Debug print
    
    # Create S3 client
    s3_client = boto3.client('s3')
    
    try:
        # Read the CSV file
        obj = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        df = pd.read_csv(obj['Body'])
        return df
        
    except Exception as e:
        print(f"Error reading file {object_key}: {str(e)}")
        raise
    
def count_records_by_file(date: str) -> Dict[str, int]:
    """
    Count records in all CSV files for a specific date folder
    
    Args:
        date (str): Date folder name (e.g., '2024-12-18')
    
    Returns:
        Dict[str, int]: Dictionary with file types as keys and record counts as values
    """
    # List of all file types
    file_types = ['accounts', 'customers', 'investments', 'transactions']
    record_counts = {}
    
    for file_type in file_types:
        try:
            # Use our existing function to read each file
            df = read_csv_from_s3(date, file_type)
            record_counts[file_type] = len(df)
        except Exception as e:
            print(f"Error reading {file_type}: {str(e)}")
            record_counts[file_type] = 0
    
    return record_counts

def analyze_folder_contents(date: str) -> None:
    """
    Analyze all CSV files in a specific date folder
    
    Args:
        date (str): Date folder name (e.g., '2024-12-18')
    """
    file_types = ['accounts', 'customers', 'investments', 'transactions']
    
    print(f"\nAnalysis for {date}:")
    print("-" * 50)
    print(f"{'File Type':12} | {'Records':>10} | {'Columns':>8} | {'Memory Usage':>12}")
    print("-" * 50)
    
    total_records = 0
    
    for file_type in file_types:
        try:
            df = read_csv_from_s3(date, file_type)
            records = len(df)
            columns = len(df.columns)
            memory = df.memory_usage(deep=True).sum() / 1024  # Convert to KB
            
            print(f"{file_type:12} | {records:10,d} | {columns:8d} | {memory:9.2f} KB")
            
            total_records += records
            
        except Exception as e:
            print(f"{file_type:12} | {'ERROR':>10} | {'ERROR':>8} | {'ERROR':>12}")
    
    print("-" * 50)
    print(f"Total Records: {total_records:,}")