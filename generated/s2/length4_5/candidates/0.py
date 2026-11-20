import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format to target string format
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    out['date'] = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Define the mapping from source hour columns to target column names
    # Source: Hour 1 to Hour 24
    # Target: 1:00 AM to 12:00 PM (with specific AM/PM logic)
    
    # Hours 1-11 map to 1:00 AM - 11:00 AM
    for h in range(1, 12):
        out[f'{h}:00 AM'] = source[f'Hour {h}']
        
    # Hour 12 maps to 12:00 AM
    out['12:00 AM'] = source['Hour 12']
    
    # Hours 13-23 map to 1:00 PM - 11:00 PM
    for h in range(13, 24):
        pm_hour = h - 12
        out[f'{pm_hour}:00 PM'] = source[f'Hour {h}']
        
    # Hour 24 maps to 12:00 PM
    out['12:00 PM'] = source['Hour 24']
    
    return out.reset_index(drop=True)
