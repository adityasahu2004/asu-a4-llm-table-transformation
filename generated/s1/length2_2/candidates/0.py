import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    # The source date format is M/D/YYYY (e.g., "7/3/2011")
    df = source.copy()
    df['date_dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Create dt_strata column formatted as M/D/YYYY (no leading zeros)
    # Using string concatenation to ensure no leading zeros for month and day
    df['dt_strata'] = (
        df['date_dt'].dt.month.astype(str) + '/' + 
        df['date_dt'].dt.day.astype(str) + '/' + 
        df['date_dt'].dt.year.astype(str)
    )
    
    # 3. Create dow column (1=Monday, ..., 7=Sunday)
    # pandas dayofweek: 0=Monday, ..., 6=Sunday
    df['dow'] = df['date_dt'].dt.dayofweek + 1
    
    # 4. Rename value columns to pct_hourly columns
    rename_map = {}
    for i in range(1, 25):
        old_col = f'value{i}'
        new_col = f'pct_hourly_{i:02d}00'
        rename_map[old_col] = new_col
    
    df = df.rename(columns=rename_map)
    
    # 5. Create pct_hourly_2500 column with value 0
    df['pct_hourly_2500'] = 0
    
    # 6. Select and order columns
    # Target columns: dt_strata, dow, pct_hourly_0100 ... pct_hourly_2500
    target_cols = ['dt_strata', 'dow']
    for i in range(1, 25):
        target_cols.append(f'pct_hourly_{i:02d}00')
    target_cols.append('pct_hourly_2500')
    
    result = df[target_cols]
    
    # 7. Ensure correct dtypes
    result['dow'] = result['dow'].astype('int64')
    result['pct_hourly_2500'] = result['pct_hourly_2500'].astype('int64')
    
    # Drop the helper datetime column if it was included (it wasn't in target_cols)
    # But we should ensure we don't return extra columns
    return result
