import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format date as requested: YYYY-MM-DD 00:00:00
    out_date = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Define mapping from source column names to target column names
    # Source: 1:00 AM ... 11:00 AM, 12:00 AM, 1:00 PM ... 11:00 PM, 12:00 PM
    # Target: Hr 1 ... Hr 24
    
    mapping = {}
    
    # 1:00 AM to 11:00 AM -> Hr 1 to Hr 11
    for h in range(1, 12):
        mapping[f'{h}:00 AM'] = f'Hr {h}'
        
    # 12:00 AM is Noon -> Hr 12
    mapping['12:00 AM'] = 'Hr 12'
    
    # 1:00 PM to 11:00 PM -> Hr 13 to Hr 23
    for h in range(1, 12):
        mapping[f'{h}:00 PM'] = f'Hr {h + 12}'
        
    # 12:00 PM is Midnight -> Hr 24
    mapping['12:00 PM'] = 'Hr 24'
    
    # Select and rename columns
    out_df = source[list(mapping.keys())].rename(columns=mapping)
    
    # Add the date column
    out_df.insert(0, 'Date', out_date)
    
    # Ensure correct column order: Date, Hr 1, ..., Hr 24
    cols = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    out_df = out_df[cols]
    
    return out_df.reset_index(drop=True)
