import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date string into datetime
    # Source format: "Thu 10/01/2009" -> %a %m/%d/%Y
    dates = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Format the date for the target column 'cst'
    # Target format: "Wed 01/01/2003" -> %a %m/%d/%Y
    out = pd.DataFrame()
    out['cst'] = dates.dt.strftime('%a %m/%d/%Y')
    
    # Map source hour columns to target hour columns
    # Source: 1:00, 2:00, ..., 23:00, 24:00:00
    # Target: 1:00, 2:00, ..., 23:00, 24:00
    
    for h in range(1, 24):
        out[f'{h}:00'] = source[f'{h}:00']
    
    # Handle the 24th hour specifically due to name change
    out['24:00'] = source['24:00:00']
    
    return out
