import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Extract Month Name
    out['month'] = dates.dt.strftime('%B')
    
    # Derive Day Type: weekday/weekend
    # pandas dayofweek: Monday=0 ... Sunday=6
    dow = dates.dt.dayofweek
    out['daytype'] = np.where(dow >= 5, 'weekend', 'weekday')
    
    # Map hourly columns
    # Source columns are '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns are 'hr1', 'hr2', ..., 'hr24'
    
    for h in range(1, 24):
        src_col = f'{h}:00'
        tgt_col = f'hr{h}'
        out[tgt_col] = source[src_col]
        
    # Handle the 24th hour specifically as it has a different source name format
    out['hr24'] = source['24:00:00']
    
    return out.reset_index(drop=True)
