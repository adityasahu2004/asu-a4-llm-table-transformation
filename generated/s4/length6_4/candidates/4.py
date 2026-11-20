import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse and format the date column
    # Source format: "M/D/YYYY" (e.g., "7/3/2014")
    # Target format: "YYYY-MM-DD 00:00:00"
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    out = pd.DataFrame()
    out['Date'] = dates.dt.strftime('%Y-%m-%d 00:00:00')

    # 2. Define mapping from source 12-hour AM/PM columns to target 24-hour Hr N columns
    # Source columns: '1:00 AM', '2:00 AM', ..., '12:00 PM', '1:00 PM', ..., '11:00 PM', '12:00 AM'
    # Note: In 24h convention for hourly buckets:
    # 1:00 AM is hour 1
    # 12:00 PM (Noon) is hour 12
    # 1:00 PM is hour 13
    # 12:00 AM (Midnight) is hour 24
    
    col_mapping = {}
    
    # AM hours: 1:00 AM to 11:00 AM -> Hr 1 to Hr 11
    for h in range(1, 12):
        col_mapping[f'{h}:00 AM'] = f'Hr {h}'
        
    # Noon: 12:00 PM -> Hr 12
    col_mapping['12:00 PM'] = 'Hr 12'
    
    # PM hours: 1:00 PM to 11:00 PM -> Hr 13 to Hr 23
    for h in range(1, 12):
        col_mapping[f'{h}:00 PM'] = f'Hr {h + 12}'
        
    # Midnight: 12:00 AM -> Hr 24
    col_mapping['12:00 AM'] = 'Hr 24'

    # 3. Select and rename columns
    # We iterate in order of target columns to ensure correct column order if necessary, 
    # though renaming handles the keys.
    for src_col, tgt_col in col_mapping.items():
        out[tgt_col] = source[src_col].values

    # 4. Ensure column order matches target spec
    target_cols = ['Date'] + [f'Hr {h}' for h in range(1, 25)]
    out = out[target_cols]
    
    return out.reset_index(drop=True)
