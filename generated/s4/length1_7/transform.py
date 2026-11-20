import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Source format: "Thu 10/01/2009" -> %a %m/%d/%Y
    dates = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Format to target cst: "Wed 01/01/2003" -> %a %m/%d/%Y
    cst_series = dates.dt.strftime('%a %m/%d/%Y')
    
    # Build the result dataframe
    result = pd.DataFrame()
    result['cst'] = cst_series
    
    # Map hourly columns
    # Source: 1:00 ... 23:00, 24:00:00
    # Target: 1:00 ... 24:00
    
    # Hours 1 to 23
    for h in range(1, 24):
        result[f'{h}:00'] = source[f'{h}:00']
        
    # Hour 24
    result['24:00'] = source['24:00:00']
    
    return result.reset_index(drop=True)
