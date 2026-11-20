import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Create the output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Format date as MM/DD/YYYY
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Map hours 1-11 to AM
    for h in range(1, 12):
        out[f'{h}:00 AM'] = source[f'{h}:00']
        
    # Map hour 12 to AM (Midnight)
    out['12:00 AM'] = source['12:00']
    
    # Map hours 13-23 to PM (13->1, 14->2, ..., 23->11)
    for h in range(13, 24):
        pm_hour = h - 12
        out[f'{pm_hour}:00 PM'] = source[f'{h}:00']
        
    # Map hour 24 to PM (Noon)
    out['12:00 PM'] = source['24:00:00']
    
    return out.reset_index(drop=True)
