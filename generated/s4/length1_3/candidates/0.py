import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create the output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Format the date as "DayOfWeek MM/DD/YYYY"
    out['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # Define the mapping from source column names to target column names
    # Source: 1:00 AM ... 11:00 AM, 12:00 PM, 1:00 PM ... 11:00 PM, 12:00 AM
    # Target: 1:00 ... 24:00
    
    # Mapping for AM hours (1-11)
    for h in range(1, 12):
        out[f'{h}:00'] = source[f'{h}:00 AM']
        
    # Mapping for 12:00 PM
    out['12:00'] = source['12:00 PM']
    
    # Mapping for PM hours (1-11) -> 13:00 - 23:00
    for h in range(1, 12):
        target_h = h + 12
        out[f'{target_h}:00'] = source[f'{h}:00 PM']
        
    # Mapping for 12:00 AM -> 24:00
    out['24:00'] = source['12:00 AM']
    
    # Reset index to ensure clean integer index
    return out.reset_index(drop=True)
