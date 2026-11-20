import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format to 'Day MM/DD/YYYY'
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    out = pd.DataFrame()
    out['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # Define mapping from source column names to target column names (1:00 to 24:00)
    # Source format: "H:00 AM/PM"
    # Target format: "H:00" where H is 1-24
    
    mapping = {}
    # AM hours: 1-11 map to 1-11
    for h in range(1, 12):
        mapping[f'{h}:00 AM'] = f'{h}:00'
    # 12:00 PM maps to 12:00
    mapping['12:00 PM'] = '12:00'
    # PM hours: 1-11 map to 13-23
    for h in range(1, 12):
        mapping[f'{h}:00 PM'] = f'{h+12}:00'
    # 12:00 AM maps to 24:00
    mapping['12:00 AM'] = '24:00'
    
    # Create the 24 hour columns in order
    for h in range(1, 25):
        target_col = f'{h}:00'
        # Find the source column name for this target
        src_col = None
        for s, t in mapping.items():
            if t == target_col:
                src_col = s
                break
        if src_col and src_col in source.columns:
            out[target_col] = source[src_col]
            
    return out.reset_index(drop=True)
