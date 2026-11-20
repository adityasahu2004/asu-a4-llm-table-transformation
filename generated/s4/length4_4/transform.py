import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates to ensure consistent handling
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Format date as MM/DD/YYYY
    out = pd.DataFrame()
    out['date'] = dates.dt.strftime('%m/%d/%Y')
    
    # Mapping from source integer columns to target time string columns
    # Source: 1, 2, ..., 11, 12, 13, ..., 23, 24
    # Target: 1:00 AM ... 11:00 AM, 12:00 AM, 1:00 PM ... 11:00 PM, 12:00 PM
    
    # Construct the mapping dictionary
    col_map = {}
    
    # 1-11: AM
    for h in range(1, 12):
        col_map[str(h)] = f"{h}:00 AM"
        
    # 12: 12:00 AM (Midnight)
    col_map['12'] = "12:00 AM"
    
    # 13-23: PM (1:00 PM to 11:00 PM)
    for h in range(13, 24):
        pm_hour = h - 12
        col_map[str(h)] = f"{pm_hour}:00 PM"
        
    # 24: 12:00 PM (Noon)
    col_map['24'] = "12:00 PM"
    
    # Apply renaming
    # Select only the hour columns from source
    hour_cols = [str(h) for h in range(1, 25)]
    subset = source[hour_cols]
    renamed = subset.rename(columns=col_map)
    
    # Define the target column order
    target_hour_cols = [
        "1:00 AM", "2:00 AM", "3:00 AM", "4:00 AM", "5:00 AM", "6:00 AM", 
        "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", 
        "12:00 AM", 
        "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM", 
        "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM", 
        "12:00 PM"
    ]
    
    # Combine date and renamed hours
    for col in target_hour_cols:
        out[col] = renamed[col]
        
    return out.reset_index(drop=True)
