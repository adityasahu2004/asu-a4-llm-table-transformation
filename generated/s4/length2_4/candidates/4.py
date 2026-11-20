import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create the output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Format dt_strata as MM/DD/YYYY
    out['dt_strata'] = dt.dt.strftime('%m/%d/%Y')
    
    # Calculate dow: Monday=0, Sunday=6
    out['dow'] = dt.dt.weekday.astype(int)
    
    # Map hourly columns 1-24 to pct_hourly_0100-2400
    for h in range(1, 25):
        out[f'pct_hourly_{h:02d}00'] = source[str(h)]
        
    # Add the 25th hour column as NaN
    out['pct_hourly_2500'] = np.nan
    
    return out.reset_index(drop=True)
