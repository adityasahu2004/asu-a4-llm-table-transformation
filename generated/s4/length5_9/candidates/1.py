import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column from M/D/YYYY format
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Format to YYYY-MM-DD 00:00:00
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Map Hr 1..24 to value1..value24
    for i in range(1, 25):
        source_col = f'Hr {i}'
        target_col = f'value{i}'
        out[target_col] = source[source_col]
        
    return out.reset_index(drop=True)
