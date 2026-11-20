import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Initialize output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Format date string
    out['dt_strata'] = dates.dt.strftime('%m/%d/%Y')
    
    # Calculate Day of Week (Monday=0, ..., Sunday=6)
    out['dow'] = dates.dt.dayofweek
    
    # Mapping from source column names to target hour indices
    # 1 AM -> 0100, ..., 11 AM -> 1100
    # 12 PM -> 1200
    # 1 PM -> 1300, ..., 11 PM -> 2300
    # 12 AM -> 2400
    
    mapping = {}
    
    # Morning hours 1-11 AM
    for h in range(1, 12):
        mapping[f'{h}:00 AM'] = f'pct_hourly_{h:02d}00'
        
    # Noon
    mapping['12:00 PM'] = 'pct_hourly_1200'
    
    # Afternoon/Evening hours 1-11 PM
    for h in range(1, 12):
        mapping[f'{h}:00 PM'] = f'pct_hourly_{h+12:02d}00'
        
    # Midnight
    mapping['12:00 AM'] = 'pct_hourly_2400'
    
    # Apply mapping
    for src_col, tgt_col in mapping.items():
        out[tgt_col] = source[src_col]
        
    # Append the constant 25th hour column
    out['pct_hourly_2500'] = 0
    
    return out.reset_index(drop=True)
