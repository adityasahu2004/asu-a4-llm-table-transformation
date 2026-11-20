import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Format cst column
    out = pd.DataFrame()
    out['cst'] = dates.dt.strftime('%a %m/%d/%Y')
    
    # Map hourly columns
    # Source has 1:00 to 23:00 and 24:00:00
    # Target has 1:00 to 24:00
    
    # Hours 1 to 23
    for h in range(1, 24):
        col_name = f'{h}:00'
        out[col_name] = source[col_name]
        
    # Hour 24
    # Source is '24:00:00', Target is '24:00'
    out['24:00'] = source['24:00:00']
    
    # Ensure correct column order
    columns = ['cst'] + [f'{h}:00' for h in range(1, 25)]
    return out[columns]
