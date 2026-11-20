import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and shift back 6 months
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    shifted_dt = dt - pd.DateOffset(months=6)
    
    out = pd.DataFrame()
    out['dt_strata'] = shifted_dt.dt.strftime('%m/%d/%Y')
    out['dow'] = shifted_dt.dt.weekday
    
    # Rename hourly columns
    for h in range(1, 25):
        src_col = f'Hour {h}'
        tgt_col = f'pct_hourly_{h:02d}00'
        out[tgt_col] = source[src_col]
        
    # Add 25th hour as NaN
    out['pct_hourly_2500'] = np.nan
    
    return out
