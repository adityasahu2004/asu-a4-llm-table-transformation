import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the CST column to datetime
    dt = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    # Create the date column formatted as MM/DD/YYYY
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Map hours 1-11 to AM
    for h in range(1, 12):
        out[f'{h}:00 AM'] = source[f'{h}:00']
        
    # Map hour 24 (24:00:00) to 12:00 AM (Midnight)
    # Note: In 12-hour clock, 12:00:00 AM is midnight. 
    # The target schema places '12:00 AM' after '11:00 AM' and before '1:00 PM'.
    out['12:00 AM'] = source['24:00:00']
    
    # Map hours 13-23 to PM (1:00 PM to 11:00 PM)
    for h in range(13, 24):
        pm_hour = h - 12
        out[f'{pm_hour}:00 PM'] = source[f'{h}:00']
        
    # Map hour 12 (12:00) to 12:00 PM (Noon)
    # The target schema places '12:00 PM' at the very end.
    out['12:00 PM'] = source['12:00']
    
    # Ensure column order matches target specification exactly
    target_cols = [
        'date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM',
        '12:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM',
        '12:00 PM'
    ]
    
    return out[target_cols].reset_index(drop=True)
