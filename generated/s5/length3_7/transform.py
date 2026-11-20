import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create the target date string column
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Rename and select the hourly columns
    for h in range(1, 25):
        out[f'Hour {h}'] = source[str(h)]
        
    return out
