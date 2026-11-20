import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format date as required: YYYY-MM-DD 00:00:00
    out = pd.DataFrame()
    out['date'] = dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Map value1..value24 to Hour 1..Hour 24
    for i in range(1, 25):
        out[f'Hour {i}'] = source[f'value{i}']
        
    return out
