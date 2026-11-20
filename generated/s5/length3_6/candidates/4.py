import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format date to target string format
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Define mapping from source column names to target hour indices (1-24)
    # Source order in sample: 
    # 1:00 AM, 2:00 AM, ..., 11:00 AM, 12:00 AM, 1:00 PM, ..., 11:00 PM, 12:00 PM
    # Note: The sample shows 12:00 AM appearing after 11:00 AM. This is unusual for chronological order 
    # but we must follow the source column order or map by name.
    # Let's map by name to be safe.
    
    col_map = {
        '1:00 AM': 1, '2:00 AM': 2, '3:00 AM': 3, '4:00 AM': 4, '5:00 AM': 5, '6:00 AM': 6,
        '7:00 AM': 7, '8:00 AM': 8, '9:00 AM': 9, '10:00 AM': 10, '11:00 AM': 11,
        '12:00 PM': 12,
        '1:00 PM': 13, '2:00 PM': 14, '3:00 PM': 15, '4:00 PM': 16, '5:00 PM': 17, '6:00 PM': 18,
        '7:00 PM': 19, '8:00 PM': 20, '9:00 PM': 21, '10:00 PM': 22, '11:00 PM': 23,
        '12:00 AM': 24
    }
    
    # Create the 24 hourly columns
    for h in range(1, 25):
        # Find the source column name that maps to this hour
        src_col = [k for k, v in col_map.items() if v == h][0]
        out[f'Hour {h}'] = source[src_col]
        
    return out.reset_index(drop=True)
