import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    df = source.copy()
    df['date_dt'] = pd.to_datetime(df['date'])
    
    # 2. Create dt_strata in M/D/YYYY format
    df['dt_strata'] = df['date_dt'].dt.strftime('%m/%d/%Y')
    
    # 3. Create dow (0=Sunday, 1=Monday, ..., 6=Saturday)
    # Python weekday(): Mon=0, ..., Sun=6
    # We want Sun=0, Mon=1, ..., Sat=6
    # Formula: (weekday() + 1) % 7
    df['dow'] = (df['date_dt'].dt.weekday() + 1) % 7
    
    # 4. Map hourly columns
    # Define the mapping from source column names to target column names
    col_mapping = {
        '1:00 AM': 'pct_hourly_0100',
        '2:00 AM': 'pct_hourly_0200',
        '3:00 AM': 'pct_hourly_0300',
        '4:00 AM': 'pct_hourly_0400',
        '5:00 AM': 'pct_hourly_0500',
        '6:00 AM': 'pct_hourly_0600',
        '7:00 AM': 'pct_hourly_0700',
        '8:00 AM': 'pct_hourly_0800',
        '9:00 AM': 'pct_hourly_0900',
        '10:00 AM': 'pct_hourly_1000',
        '11:00 AM': 'pct_hourly_1100',
        '12:00 PM': 'pct_hourly_1200',
        '1:00 PM': 'pct_hourly_1300',
        '2:00 PM': 'pct_hourly_1400',
        '3:00 PM': 'pct_hourly_1500',
        '4:00 PM': 'pct_hourly_1600',
        '5:00 PM': 'pct_hourly_1700',
        '6:00 PM': 'pct_hourly_1800',
        '7:00 PM': 'pct_hourly_1900',
        '8:00 PM': 'pct_hourly_2000',
        '9:00 PM': 'pct_hourly_2100',
        '10:00 PM': 'pct_hourly_2200',
        '11:00 PM': 'pct_hourly_2300',
        '12:00 AM': 'pct_hourly_2400'
    }
    
    # Rename the columns
    df = df.rename(columns=col_mapping)
    
    # 5. Add the constant column pct_hourly_2500
    df['pct_hourly_2500'] = 0
    
    # 6. Select and order the columns as per target schema
    target_cols = [
        'dt_strata', 'dow',
        'pct_hourly_0100', 'pct_hourly_0200', 'pct_hourly_0300', 'pct_hourly_0400',
        'pct_hourly_0500', 'pct_hourly_0600', 'pct_hourly_0700', 'pct_hourly_0800',
        'pct_hourly_0900', 'pct_hourly_1000', 'pct_hourly_1100', 'pct_hourly_1200',
        'pct_hourly_1300', 'pct_hourly_1400', 'pct_hourly_1500', 'pct_hourly_1600',
        'pct_hourly_1700', 'pct_hourly_1800', 'pct_hourly_1900', 'pct_hourly_2000',
        'pct_hourly_2100', 'pct_hourly_2200', 'pct_hourly_2300', 'pct_hourly_2400',
        'pct_hourly_2500'
    ]
    
    result = df[target_cols]
    
    # Ensure dtypes match target if necessary
    # dow is int64
    result['dow'] = result['dow'].astype('int64')
    # pct_hourly_2500 is int64
    result['pct_hourly_2500'] = result['pct_hourly_2500'].astype('int64')
    # dt_strata is str
    result['dt_strata'] = result['dt_strata'].astype('str')
    
    return result
