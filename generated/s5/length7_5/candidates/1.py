import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Derive month and daytype
    out = pd.DataFrame(index=source.index)
    out['month'] = dates.dt.strftime('%B')
    # dayofweek: 0=Monday, ..., 6=Sunday. Weekend if >= 5
    out['daytype'] = np.where(dates.dt.dayofweek >= 5, 'weekend', 'weekday')
    
    # Define the mapping from source column names to target hour indices (1-24)
    # Source order: 1AM..11AM, 12AM(Noon), 1PM..11PM, 12PM(Midnight)
    # Target order: hr1..hr24 chronologically
    
    # Mapping: Source Column Name -> Target Column Name
    hour_map = {}
    
    # 1 AM to 11 AM -> hr1 to hr11
    for h in range(1, 12):
        hour_map[f'{h}:00 AM'] = f'hr{h}'
        
    # 12 AM (Noon) -> hr12
    hour_map['12:00 AM'] = 'hr12'
    
    # 1 PM to 11 PM -> hr13 to hr23
    for h in range(1, 12):
        hour_map[f'{h}:00 PM'] = f'hr{h + 12}'
        
    # 12 PM (Midnight) -> hr24
    hour_map['12:00 PM'] = 'hr24'
    
    # Apply mapping
    for src_col, tgt_col in hour_map.items():
        out[tgt_col] = source[src_col]
        
    return out.reset_index(drop=True)
