import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column to ensure consistent formatting MM/DD/YYYY
    # The source format is "%a %m/%d/%Y" e.g., "Thu 10/01/2009"
    dt = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Create the output dataframe
    out = pd.DataFrame(index=source.index)
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Map hours 1-11 to 1 AM - 11 AM
    for h in range(1, 12):
        out[f'{h}:00 AM'] = source[f'{h}:00']
        
    # Map hour 12 (Noon) to the target column named "12:00 AM" based on positional logic
    out['12:00 AM'] = source['12:00']
    
    # Map hours 13-23 to 1 PM - 11 PM
    # Source 13:00 is 1 PM, Source 23:00 is 11 PM
    for h in range(13, 24):
        pm_hour = h - 12
        out[f'{pm_hour}:00 PM'] = source[f'{h}:00']
        
    # Map hour 24:00:00 (Midnight) to the target column named "12:00 PM" based on positional logic
    out['12:00 PM'] = source['24:00:00']
    
    # Reorder columns to match target schema exactly
    target_cols = [
        'date',
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM',
        '12:00 AM',
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM',
        '12:00 PM'
    ]
    
    return out[target_cols].reset_index(drop=True)
