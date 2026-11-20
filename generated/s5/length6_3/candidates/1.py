import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create the target DataFrame
    out = pd.DataFrame()
    out['Date'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Map value1...value24 to Hr 1...Hr 24
    for i in range(1, 25):
        out[f'Hr {i}'] = source[f'value{i}']
        
    return out.reset_index(drop=True)
