import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse CST to datetime to extract date
    dt = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Define mapping from source hour columns to target AM/PM columns
    # Source columns: 1:00 to 24:00:00
    # Target columns: 1:00 AM ... 11:00 AM, 12:00 AM, 1:00 PM ... 11:00 PM, 12:00 PM
    
    mapping = {}
    
    # Hours 1-11 map to 1:00 AM - 11:00 AM
    for h in range(1, 12):
        mapping[f'{h}:00'] = f'{h}:00 AM'
        
    # Hour 12 maps to 12:00 AM
    mapping['12:00'] = '12:00 AM'
    
    # Hours 13-23 map to 1:00 PM - 11:00 PM
    for h in range(13, 24):
        target_h = h - 12
        mapping[f'{h}:00'] = f'{target_h}:00 PM'
        
    # Hour 24 maps to 12:00 PM
    mapping['24:00:00'] = '12:00 PM'
    
    # Rename and select columns
    out = out.join(source.rename(columns=mapping)[list(mapping.values())])
    
    return out.reset_index(drop=True)
