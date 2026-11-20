import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the source date
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Construct the output DataFrame
    out = pd.DataFrame(index=source.index)
    
    # Format dt_strata as MM/DD/YYYY
    out['dt_strata'] = dates.dt.strftime('%m/%d/%Y')
    
    # Calculate dow: Monday=0, ..., Sunday=6
    out['dow'] = dates.dt.dayofweek.astype('int64')
    
    # Map hours 1-24
    for h in range(1, 25):
        src_col = str(h)
        tgt_col = f'pct_hourly_{h:02d}00'
        out[tgt_col] = source[src_col]
        
    # Add the 25th hour column as null
    out['pct_hourly_2500'] = np.nan
    
    # Reset index to match target schema expectations (default integer index)
    return out.reset_index(drop=True)
