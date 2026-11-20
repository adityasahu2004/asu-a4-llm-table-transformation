import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame by:
    1. Selecting date and value columns.
    2. Renaming columns to match target schema.
    3. Parsing and formatting the date column.
    4. Sorting by date.
    """
    # Define the mapping for value columns
    value_cols = [f"value{i}" for i in range(1, 25)]
    target_hour_cols = [f"Hr {i}" for i in range(1, 25)]
    
    # Select relevant columns
    df = source[['date'] + value_cols].copy()
    
    # Rename columns
    df.rename(columns={
        'date': 'Date',
        **{f"value{i}": f"Hr {i}" for i in range(1, 25)}
    }, inplace=True)
    
    # Parse dates and format to target string format
    # Source format: MM/DD/YYYY
    # Target format: YYYY-MM-DD HH:MM:SS
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Sort by Date to match target order
    # We need to sort by the actual datetime value, so we parse again temporarily or sort by string if format is ISO-like
    # Since the string format is YYYY-MM-DD..., lexicographical sort works, but let's be safe with datetime
    df['Date_dt'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date_dt', inplace=True)
    df.drop(columns=['Date_dt'], inplace=True)
    
    # Reset index to ensure clean output
    df.reset_index(drop=True, inplace=True)
    
    return df
