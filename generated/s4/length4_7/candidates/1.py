import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Create the output dataframe with the formatted date
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Define the mapping from source column names to target column names
    # Source: 1:00 ... 11:00, 12:00, 13:00 ... 23:00, 24:00:00
    # Target: 1:00 AM ... 11:00 AM, 12:00 AM, 1:00 PM ... 11:00 PM, 12:00 PM
    
    rename_map = {}
    
    # Hours 1-11 map to AM
    for h in range(1, 12):
        rename_map[f'{h}:00'] = f'{h}:00 AM'
        
    # Hour 12 maps to 12:00 AM based on position in target schema
    rename_map['12:00'] = '12:00 AM'
    
    # Hours 13-23 map to PM (13->1, ..., 23->11)
    for h in range(13, 24):
        pm_h = h - 12
        rename_map[f'{h}:00'] = f'{pm_h}:00 PM'
        
    # Hour 24 maps to 12:00 PM
    rename_map['24:00:00'] = '12:00 PM'
    
    # Select and rename the hour columns
    hour_cols = [f'{h}:00' for h in range(1, 24)] + ['24:00:00']
    out = pd.concat([out, source[hour_cols].rename(columns=rename_map)], axis=1)
    
    # Ensure column order matches target specification
    target_cols = ['date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', 
                   '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', 
                   '12:00 AM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', 
                   '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', 
                   '12:00 PM']
                   
    return out[target_cols].reset_index(drop=True)
