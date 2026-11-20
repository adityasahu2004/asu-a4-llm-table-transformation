import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    dates = pd.to_datetime(source['Date'])
    
    # Format dt_strata as M/D/YYYY (no leading zeros)
    # strftime('%m/%d/%Y') gives MM/DD/YYYY
    # We convert to int and back to string to remove leading zeros
    dt_strata = dates.apply(lambda x: f"{x.month}/{x.day}/{x.year}")
    
    # Calculate day of week (Monday=0, ..., Sunday=6)
    dow = dates.dt.dayofweek
    
    # Map hourly columns
    out = pd.DataFrame()
    out['dt_strata'] = dt_strata
    out['dow'] = dow
    
    for h in range(1, 25):
        src_col = f'Hr {h}'
        tgt_col = f'pct_hourly_{h:02d}00'
        out[tgt_col] = source[src_col]
        
    # Add the constant 25th hour column
    out['pct_hourly_2500'] = 0
    
    return out
