import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format the date to the target string format
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Map value1..value24 to Hour 1..Hour 24
    for i in range(1, 25):
        out[f'Hour {i}'] = source[f'value{i}']
        
    return out.reset_index(drop=True)
