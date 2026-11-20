import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date to extract DOW and format string
    dt_series = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame()
    
    # 1. dt_strata: formatted date string MM/DD/YYYY
    out['dt_strata'] = dt_series.dt.strftime('%m/%d/%Y')
    
    # 2. dow: integer day of week (0=Monday, 6=Sunday)
    out['dow'] = dt_series.dt.weekday
    
    # 3. Hourly columns: Rename Hr 1..24 to pct_hourly_0100..2400
    for h in range(1, 25):
        source_col = f'Hr {h}'
        target_col = f'pct_hourly_{h:02d}00'
        out[target_col] = source[source_col]
        
    # 4. pct_hourly_2500: Constant 0
    out['pct_hourly_2500'] = 0
    
    return out.reset_index(drop=True)
