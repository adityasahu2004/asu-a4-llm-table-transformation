import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format date to target string format
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Define the mapping from source column names to target column names
    # Source order: 1AM, 2AM, ..., 11AM, 12AM, 1PM, ..., 11PM, 12PM
    # Target order: value1 (1AM), value2 (2AM), ..., value12 (12AM), value13 (1PM), ..., value24 (12PM)
    
    # AM hours: 1-11
    for h in range(1, 12):
        out[f'value{h}'] = source[f'{h}:00 AM']
        
    # 12 AM is the 12th hour
    out['value12'] = source['12:00 AM']
    
    # PM hours: 1-11 map to 13-23
    for h in range(1, 12):
        out[f'value{h+12}'] = source[f'{h}:00 PM']
        
    # 12 PM is the 24th hour
    out['value24'] = source['12:00 PM']
    
    return out.reset_index(drop=True)
