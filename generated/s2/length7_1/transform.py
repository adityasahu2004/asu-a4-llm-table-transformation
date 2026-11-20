import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the CST column to datetime
    # Format is "DayOfWeek MM/DD/YYYY", e.g., "Sat 12/01/2012"
    dt = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    # Derive 'month': Month name padded to 10 characters
    # e.g., "April" -> "April    ", "November" -> "November "
    month_names = dt.dt.strftime('%B')
    month_padded = month_names.str.pad(10, side='right')
    
    # Derive 'daytype': weekday or weekend
    # dayofweek: Monday=0 ... Sunday=6
    is_weekend = dt.dt.dayofweek >= 5
    daytype = np.where(is_weekend, 'weekend', 'weekday')
    
    # Map hour columns
    # Source: '1:00'...'23:00', '24:00:00'
    # Target: 'hr1'...'hr24'
    hour_mapping = {}
    for h in range(1, 24):
        hour_mapping[f'{h}:00'] = f'hr{h}'
    hour_mapping['24:00:00'] = 'hr24'
    
    # Select and rename hour columns
    hour_cols = [f'hr{h}' for h in range(1, 25)]
    source_hour_cols = [f'{h}:00' for h in range(1, 24)] + ['24:00:00']
    
    out = pd.DataFrame()
    out['month'] = month_padded
    out['daytype'] = daytype
    
    for src_col, tgt_col in zip(source_hour_cols, hour_cols):
        out[tgt_col] = source[src_col]
        
    return out
