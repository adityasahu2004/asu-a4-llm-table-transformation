import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Format date to MM/DD/YYYY
    out = pd.DataFrame()
    out['Date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Rename and select hourly columns
    for h in range(1, 25):
        out[f'Hr {h}'] = source[str(h)]
        
    return out
