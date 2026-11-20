import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Format the date
    # Source format: "7/3/2015" -> Target format: "2015-01-01 00:00:00" (ISO with time)
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    out_date = dt.strftime('%Y-%m-%d 00:00:00')
    
    # 2. Define the mapping from Source Hour columns to Target Column Names
    # Source: Hour 1 ... Hour 24
    # Target: 1:00 AM ... 11:00 AM, 12:00 AM, 1:00 PM ... 11:00 PM, 12:00 PM
    
    target_cols = []
    target_col_names = []
    
    # Hours 1-11 map to 1:00 AM - 11:00 AM
    for h in range(1, 12):
        target_cols.append(f'Hour {h}')
        target_col_names.append(f'{h}:00 AM')
        
    # Hour 12 maps to 12:00 AM (based on target schema/sample alignment)
    target_cols.append('Hour 12')
    target_col_names.append('12:00 AM')
    
    # Hours 13-23 map to 1:00 PM - 11:00 PM
    for h in range(13, 24):
        target_cols.append(f'Hour {h}')
        target_col_names.append(f'{h-12}:00 PM')
        
    # Hour 24 maps to 12:00 PM
    target_cols.append('Hour 24')
    target_col_names.append('12:00 PM')
    
    # 3. Construct the output DataFrame
    # Initialize with the date column
    result = pd.DataFrame({'date': out_date}, index=source.index)
    
    # Add the hourly columns in the specified order
    for src_col, tgt_col in zip(target_cols, target_col_names):
        result[tgt_col] = source[src_col]
        
    return result.reset_index(drop=True)
