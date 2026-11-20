import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Initialize result dataframe
    result = pd.DataFrame(index=source.index)
    
    # Create dt_strata column formatted as MM/DD/YYYY
    result['dt_strata'] = dates.dt.strftime('%m/%d/%Y')
    
    # Create dow column (0=Monday, 6=Sunday)
    result['dow'] = dates.dt.dayofweek
    
    # Map hourly columns Hr 1...Hr 24 to pct_hourly_0100...pct_hourly_2400
    for h in range(1, 25):
        src_col = f'Hr {h}'
        tgt_col = f'pct_hourly_{h:02d}00'
        result[tgt_col] = source[src_col]
        
    # Add the constant 25th hour column
    result['pct_hourly_2500'] = 0
    
    return result.reset_index(drop=True)
