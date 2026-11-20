import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create the cst column with format "DayOfWeek MM/DD/YYYY"
    out = pd.DataFrame()
    out['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # Define the mapping from source AM/PM columns to target 24-hour labels
    # Source columns: 1:00 AM ... 11:00 AM, 12:00 AM, 1:00 PM ... 11:00 PM, 12:00 PM
    # Target columns: 1:00 ... 24:00
    
    # Mapping dictionary
    col_map = {}
    
    # 1:00 AM to 11:00 AM -> 1:00 to 11:00
    for h in range(1, 12):
        col_map[f'{h}:00 AM'] = f'{h}:00'
        
    # 12:00 PM -> 12:00
    col_map['12:00 PM'] = '12:00'
    
    # 1:00 PM to 11:00 PM -> 13:00 to 23:00
    for h in range(1, 12):
        col_map[f'{h}:00 PM'] = f'{h+12}:00'
        
    # 12:00 AM -> 24:00
    col_map['12:00 AM'] = '24:00'
    
    # Apply the mapping
    out = out.join(source[list(col_map.keys())].rename(columns=col_map))
    
    # Ensure column order matches target specification (1:00 to 24:00)
    hour_cols = [f'{h}:00' for h in range(1, 25)]
    out = out[['cst'] + hour_cols]
    
    return out.reset_index(drop=True)
