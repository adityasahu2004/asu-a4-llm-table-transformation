import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # dt_strata: formatted date string
    out['dt_strata'] = dates.dt.strftime('%m/%d/%Y')
    
    # dow: ISO weekday (Mon=1, Sun=7)
    out['dow'] = dates.dt.isocalendar().week # Not needed, just dayofweek
    out['dow'] = dates.dt.dayofweek + 1
    
    # Rename value1-24 to pct_hourly_0100-2400
    for h in range(1, 25):
        src_col = f'value{h}'
        tgt_col = f'pct_hourly_{h:02d}00'
        out[tgt_col] = source[src_col]
        
    # Add constant zero column for 25th hour
    out['pct_hourly_2500'] = 0
    
    # Ensure correct column order
    cols = ['dt_strata', 'dow'] + [f'pct_hourly_{h:02d}00' for h in range(1, 26)]
    out = out[cols]
    
    # Ensure dtypes match target (dow int64, pct_hourly_2500 int64, others float64)
    out['dow'] = out['dow'].astype('int64')
    out['pct_hourly_2500'] = out['pct_hourly_2500'].astype('int64')
    
    return out.reset_index(drop=True)
