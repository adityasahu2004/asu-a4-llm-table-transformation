import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column using the observed format m/d/Y
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Format the date as requested in the target schema
    out = pd.DataFrame()
    out['date'] = dates.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Map source hour columns to target value columns
    # Source columns are 'Hr 1' to 'Hr 24'
    # Target columns are 'value1' to 'value24'
    for i in range(1, 25):
        source_col = f'Hr {i}'
        target_col = f'value{i}'
        out[target_col] = source[source_col]
        
    return out
