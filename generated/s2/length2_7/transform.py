import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    dates = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    out = pd.DataFrame(index=source.index)
    out['dt_strata'] = dates.dt.strftime('%m/%d/%y')
    out['dow'] = dates.dt.dayofweek + 1
    
    for h in range(1, 25):
        src_col = f'{h}:00' if h < 24 else '24:00:00'
        out[f'pct_hourly_{h:02d}00'] = source[src_col]
        
    out['pct_hourly_2500'] = np.nan
    
    return out.reset_index(drop=True)
