import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format as MM/DD/YYYY
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    out = pd.DataFrame()
    out['date'] = dates.dt.strftime('%m/%d/%Y')
    
    # Map source hours (1-24) to target column names
    # Source 1-11 -> 1-11 AM
    for h in range(1, 12):
        out[f'{h}:00 AM'] = source[str(h)]
        
    # Source 24 -> 12:00 AM (Midnight)
    out['12:00 AM'] = source['24']
    
    # Source 13-23 -> 1-11 PM
    for h in range(13, 24):
        pm_hour = h - 12
        out[f'{pm_hour}:00 PM'] = source[str(h)]
        
    # Source 12 -> 12:00 PM (Noon)
    out['12:00 PM'] = source['12']
    
    # Ensure column order matches target specification
    target_cols = [
        'date',
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM',
        '12:00 AM',
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM',
        '12:00 PM'
    ]
    
    return out[target_cols].reset_index(drop=True)
