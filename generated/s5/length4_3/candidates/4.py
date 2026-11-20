import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    dates = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    out['date'] = dates.dt.strftime('%m/%d/%Y')
    
    # Define mapping from source column suffix to target column name
    # Source: 0100-2400
    # Target: 1:00 AM - 11:00 AM, 12:00 AM, 1:00 PM - 11:00 PM, 12:00 PM
    
    mapping = {}
    # 1-11 AM
    for h in range(1, 12):
        mapping[f'PCT_HOURLY_{h:02d}00'] = f'{h}:00 AM'
    # 12 -> 12:00 AM (based on target column order: 12th col is 12:00 AM)
    mapping['PCT_HOURLY_1200'] = '12:00 AM'
    # 13-23 -> 1:00 PM - 11:00 PM
    for h in range(13, 24):
        hour_12 = h - 12
        mapping[f'PCT_HOURLY_{h:02d}00'] = f'{hour_12}:00 PM'
    # 24 -> 12:00 PM (based on target column order: 24th col is 12:00 PM)
    mapping['PCT_HOURLY_2400'] = '12:00 PM'
    
    # Apply mapping
    for src_col, tgt_col in mapping.items():
        out[tgt_col] = source[src_col]
        
    return out.reset_index(drop=True)
