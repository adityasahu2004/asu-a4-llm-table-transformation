import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column to extract date components and day of week
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Initialize the output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Format date as MM/DD/YYYY for dt_strata
    out['dt_strata'] = dates.dt.strftime('%m/%d/%Y')
    
    # Calculate ISO day of week (Monday=1, Sunday=7)
    out['dow'] = dates.dt.dayofweek + 1
    
    # Map value1..value24 to pct_hourly_0100..pct_hourly_2400
    for h in range(1, 25):
        src_col = f'value{h}'
        tgt_col = f'pct_hourly_{h:02d}00'
        out[tgt_col] = source[src_col]
        
    # Add the constant 25th hour column
    out['pct_hourly_2500'] = 0
    
    return out.reset_index(drop=True)
