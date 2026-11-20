import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Format dt_strata as M/D/YYYY
    out['dt_strata'] = dates.dt.strftime('%m/%d/%Y')
    
    # Calculate dow (0=Monday, ..., 6=Sunday)
    out['dow'] = dates.dt.dayofweek
    
    # Map Hour 1..24 to pct_hourly_0100..pct_hourly_2400
    for h in range(1, 25):
        src_col = f'Hour {h}'
        tgt_col = f'pct_hourly_{h:02d}00'
        out[tgt_col] = source[src_col]
        
    # Add pct_hourly_2500 with NaNs
    out['pct_hourly_2500'] = np.nan
    
    return out.reset_index(drop=True)
