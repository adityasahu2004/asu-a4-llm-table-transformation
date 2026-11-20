import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    dates = pd.to_datetime(source['date'])
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Format dt_strata as M/D/YYYY
    out['dt_strata'] = dates.dt.strftime('%-m/%-d/%Y')
    
    # Compute dow (Monday=0, Sunday=6)
    out['dow'] = dates.dt.dayofweek
    
    # Rename hourly columns
    for h in range(1, 25):
        out[f'pct_hourly_{h:02d}00'] = source[f'Hour {h}']
        
    # Add pct_hourly_2500 as NaN
    out['pct_hourly_2500'] = np.nan
    
    return out.reset_index(drop=True)
