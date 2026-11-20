import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the CST column to extract date information
    # Format is "DayName MM/DD/YYYY", e.g., "Sat 12/01/2012"
    dates = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    # Create the output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Format dt_strata as MM/DD/YYYY
    out['dt_strata'] = dates.dt.strftime('%m/%d/%Y')
    
    # Calculate dow (ISO weekday: Monday=1, Sunday=7)
    out['dow'] = dates.dt.dayofweek + 1
    
    # Map the 24 hourly columns
    # Source names: "1:00", "2:00", ..., "23:00", "24:00:00"
    # Target names: "pct_hourly_0100", ..., "pct_hourly_2400"
    for h in range(1, 25):
        if h < 24:
            src_col = f"{h}:00"
        else:
            src_col = "24:00:00"
        
        tgt_col = f"pct_hourly_{h:02d}00"
        out[tgt_col] = source[src_col]
        
    # Add the constant column for hour 25
    out['pct_hourly_2500'] = 0
    
    # Ensure integer type for dow and pct_hourly_2500 if necessary, 
    # though pandas usually infers float for data frames with floats.
    # The target schema specifies int64 for dow and pct_hourly_2500.
    out['dow'] = out['dow'].astype('int64')
    out['pct_hourly_2500'] = out['pct_hourly_2500'].astype('int64')
    
    return out.reset_index(drop=True)
