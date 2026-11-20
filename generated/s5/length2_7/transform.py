import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    dt = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Format date string
    out['dt_strata'] = dt.dt.strftime('%m/%d/%y')
    
    # Derive day of week (ISO: Mon=1, Sun=7)
    out['dow'] = dt.dt.dayofweek + 1
    
    # Map hourly columns
    for h in range(1, 25):
        src_col = f'{h}:00' if h < 24 else '24:00:00'
        tgt_col = f'pct_hourly_{h:02d}00'
        out[tgt_col] = source[src_col]
        
    # Add 25th hour as NaN
    out['pct_hourly_2500'] = np.nan
    
    return out.reset_index(drop=True)
