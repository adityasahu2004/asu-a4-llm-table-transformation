import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format date as required by target: YYYY-MM-DD 00:00:00
    out = pd.DataFrame()
    out['date'] = dt.strftime('%Y-%m-%d 00:00:00')
    
    # Define the mapping from source value columns to target hour columns
    # Target order: 1:00 AM ... 11:00 AM, 12:00 AM, 1:00 PM ... 11:00 PM, 12:00 PM
    
    # 1:00 AM to 11:00 AM (value1 to value11)
    for h in range(1, 12):
        out[f'{h}:00 AM'] = source[f'value{h}']
        
    # 12:00 AM (Midnight, end of day) -> value24
    out['12:00 AM'] = source['value24']
    
    # 1:00 PM to 11:00 PM (value13 to value23)
    for h in range(13, 24):
        # Convert 13-23 to 1-11 PM
        pm_h = h - 12
        out[f'{pm_h}:00 PM'] = source[f'value{h}']
        
    # 12:00 PM (Noon) -> value12
    out['12:00 PM'] = source['value12']
    
    # Reset index to match target row count style if necessary, though usually just dropping old index
    return out.reset_index(drop=True)
