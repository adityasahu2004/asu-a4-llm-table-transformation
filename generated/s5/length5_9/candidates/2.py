import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column and format it as required
    # Source format is m/d/yyyy (e.g., 1/1/2014)
    # Target format is YYYY-MM-DD 00:00:00
    out = pd.DataFrame()
    out['date'] = pd.to_datetime(source['Date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d 00:00:00')
    
    # Map Hr 1..24 to value1..value24
    for i in range(1, 25):
        out[f'value{i}'] = source[f'Hr {i}']
        
    return out
