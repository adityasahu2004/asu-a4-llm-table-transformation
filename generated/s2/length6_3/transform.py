import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format date to target string format
    out = pd.DataFrame()
    out['Date'] = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Rename value columns to Hr columns
    for i in range(1, 25):
        out[f'Hr {i}'] = source[f'value{i}']
        
    return out
