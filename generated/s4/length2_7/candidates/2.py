import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date
    dt = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Format date as MM/DD/YY
    out['dt_strata'] = dt.dt.strftime('%m/%d/%y')
    
    # Extract ISO day of week (1=Mon, 7=Sun)
    out['dow'] = dt.dt.dayofweek + 1
    
    # Map hourly columns
    for h in range(1, 24):
        src_col = f"{h}:00"
        tgt_col = f"pct_hourly_{h:02d}00"
        out[tgt_col] = source[src_col]
        
    # Handle the 24th hour specifically due to source column name '24:00:00'
    out['pct_hourly_2400'] = source['24:00:00']
    
    # Add the 25th hour as null
    out['pct_hourly_2500'] = np.nan
    
    # Define target column order
    cols = ['dt_strata', 'dow'] + [f'pct_hourly_{h:02d}00' for h in range(1, 26)]
    
    return out[cols].reset_index(drop=True)
