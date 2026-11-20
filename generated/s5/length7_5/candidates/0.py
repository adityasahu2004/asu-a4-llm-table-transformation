import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Month name
    out['month'] = dt.dt.strftime('%B')
    
    # Day type
    # dt.dayofweek: 0=Mon, ..., 5=Sat, 6=Sun
    out['daytype'] = np.where(dt.dt.dayofweek.isin([5, 6]), 'weekend', 'weekday')
    
    # Map hours
    # Source columns order: 1-11 AM, 12 AM, 1-11 PM, 12 PM
    # Target columns: hr1-24 chronological
    
    # 1:00 AM to 11:00 AM -> hr1 to hr11
    for h in range(1, 12):
        out[f'hr{h}'] = source[f'{h}:00 AM']
        
    # 12:00 PM (Noon) -> hr12
    out['hr12'] = source['12:00 PM']
    
    # 1:00 PM to 11:00 PM -> hr13 to hr23
    for h in range(1, 12):
        out[f'hr{h+12}'] = source[f'{h}:00 PM']
        
    # 12:00 AM (Midnight) -> hr24
    out['hr24'] = source['12:00 AM']
    
    return out.reset_index(drop=True)
