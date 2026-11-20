import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Format the date as required by the target schema
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Map source hourly columns to target value columns
    for i in range(1, 25):
        out[f'value{i}'] = source[f'Hr {i}']
        
    return out
