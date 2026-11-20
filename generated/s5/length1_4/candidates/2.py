import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create the output dataframe
    out = pd.DataFrame()
    
    # Format the date for the 'cst' column
    out['cst'] = dates.dt.strftime('%a %m/%d/%Y')
    
    # Rename the hourly columns from 1..24 to 1:00..24:00
    for h in range(1, 25):
        out[f'{h}:00'] = source[h]
        
    return out
