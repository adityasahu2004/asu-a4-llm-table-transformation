import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Format date as YYYY-MM-DD 00:00:00
    out['date'] = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Map hours
    # Hour 1-11: 1:00 AM - 11:00 AM
    for h in range(1, 12):
        out[f'Hour {h}'] = source[f'{h}:00 AM']
        
    # Hour 12: 12:00 PM
    out['Hour 12'] = source['12:00 PM']
    
    # Hour 13-23: 1:00 PM - 11:00 PM
    for h in range(13, 24):
        pm_hour = h - 12
        out[f'Hour {h}'] = source[f'{pm_hour}:00 PM']
        
    # Hour 24: 12:00 AM
    out['Hour 24'] = source['12:00 AM']
    
    return out.reset_index(drop=True)
