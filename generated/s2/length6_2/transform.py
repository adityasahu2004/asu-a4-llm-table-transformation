import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse CST to datetime to extract date
    # Format is "DayOfWeek MM/DD/YYYY" e.g., "Sat 12/01/2012"
    # We can parse this directly or just extract the date part.
    # Using pd.to_datetime with format is robust.
    dt = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    # Create the output dataframe
    out = pd.DataFrame()
    
    # Format date as MM/DD/YYYY
    out['Date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Map source columns to target columns
    # Source: 1:00, 2:00, ..., 23:00, 24:00:00
    # Target: Hr 1, Hr 2, ..., Hr 23, Hr 24
    
    for h in range(1, 24):
        out[f'Hr {h}'] = source[f'{h}:00']
        
    # Handle the 24th hour specifically as it has a different name in source
    out['Hr 24'] = source['24:00:00']
    
    return out
