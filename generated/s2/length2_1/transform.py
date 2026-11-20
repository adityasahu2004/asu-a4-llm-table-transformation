import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the CST column to datetime
    # Format is "DayOfWeek MM/DD/YYYY", e.g., "Sat 12/01/2012"
    dt = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    # Create dt_strata as MM/DD/YYYY
    dt_strata = dt.dt.strftime('%m/%d/%Y')
    
    # Create dow as ISO day of week (Mon=1, Sun=7)
    dow = dt.dt.dayofweek + 1
    
    # Map hour columns
    # Source: '1:00'...'23:00', '24:00:00'
    # Target: 'pct_hourly_0100'...'pct_hourly_2400'
    hour_cols = {}
    for h in range(1, 24):
        src_name = f'{h}:00'
        tgt_name = f'pct_hourly_{h:02d}00'
        hour_cols[src_name] = tgt_name
    
    # Handle the 24th hour specifically as it has seconds in source name
    hour_cols['24:00:00'] = 'pct_hourly_2400'
    
    # Rename the hour columns
    df_out = source.rename(columns=hour_cols)
    
    # Select and order columns
    # We need: dt_strata, dow, then the 24 hourly columns, then pct_hourly_2500
    
    # Construct the list of hourly columns in order
    hourly_cols_ordered = [f'pct_hourly_{h:02d}00' for h in range(1, 25)]
    
    # Build the final dataframe
    result = pd.DataFrame()
    result['dt_strata'] = dt_strata
    result['dow'] = dow
    
    for col in hourly_cols_ordered:
        result[col] = df_out[col]
        
    result['pct_hourly_2500'] = 0
    
    return result.reset_index(drop=True)
