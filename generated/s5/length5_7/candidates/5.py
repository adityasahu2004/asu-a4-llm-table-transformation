import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Format the date to the target string format
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Rename and select the hourly value columns
    for h in range(1, 25):
        out[f'value{h}'] = source[str(h)]
        
    return out.reset_index(drop=True)
