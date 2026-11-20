import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse and Format Date
    # Source format: MM/DD/YYYY
    # Target format: YYYY-MM-DD 00:00:00
    dt_series = pd.to_datetime(source['date'], format='%m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    out['Date'] = dt_series.dt.strftime('%Y-%m-%d 00:00:00')
    
    # 2. Map Hourly Columns
    # Mapping from source AM/PM names to target Hr 1-24 names
    # 12 AM is hour 1, 1 AM is hour 2, ..., 11 AM is hour 12
    # 12 PM is hour 13, 1 PM is hour 14, ..., 11 PM is hour 24
    
    mapping = {
        '12:00 AM': 'Hr 1',
        '1:00 AM': 'Hr 2',
        '2:00 AM': 'Hr 3',
        '3:00 AM': 'Hr 4',
        '4:00 AM': 'Hr 5',
        '5:00 AM': 'Hr 6',
        '6:00 AM': 'Hr 7',
        '7:00 AM': 'Hr 8',
        '8:00 AM': 'Hr 9',
        '9:00 AM': 'Hr 10',
        '10:00 AM': 'Hr 11',
        '11:00 AM': 'Hr 12',
        '12:00 PM': 'Hr 13',
        '1:00 PM': 'Hr 14',
        '2:00 PM': 'Hr 15',
        '3:00 PM': 'Hr 16',
        '4:00 PM': 'Hr 17',
        '5:00 PM': 'Hr 18',
        '6:00 PM': 'Hr 19',
        '7:00 PM': 'Hr 20',
        '8:00 PM': 'Hr 21',
        '9:00 PM': 'Hr 22',
        '10:00 PM': 'Hr 23',
        '11:00 PM': 'Hr 24'
    }
    
    # Apply mapping
    for src_col, tgt_col in mapping.items():
        out[tgt_col] = source[src_col]
        
    # 3. Ensure correct column order
    target_cols = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    out = out[target_cols]
    
    return out.reset_index(drop=True)
