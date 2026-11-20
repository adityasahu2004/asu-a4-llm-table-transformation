import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the Date column
    dates = pd.to_datetime(source['Date'])
    
    # Create the output dataframe
    out = pd.DataFrame()
    
    # dt_strata: formatted date
    out['dt_strata'] = dates.dt.strftime('%m/%d/%Y')
    
    # dow: 0=Sun, 1=Mon, ..., 6=Sat
    # pandas dayofweek: 0=Mon, ..., 6=Sun
    # mapping: Mon(0)->1, Tue(1)->2, ..., Sun(6)->0
    # formula: (dayofweek + 1) % 7
    out['dow'] = (dates.dt.dayofweek + 1) % 7
    
    # Rename hourly columns 1..24 to pct_hourly_0100..2400
    for h in range(1, 25):
        out[f'pct_hourly_{h:02d}00'] = source[str(h)]
        
    # Add the 25th hour column with NaNs
    out['pct_hourly_2500'] = np.nan
    
    return out
