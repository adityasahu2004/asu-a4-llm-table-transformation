import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date from the 'CST' column
    # Format in source: "Day MM/DD/YYYY" e.g., "Sat 12/01/2012"
    # We extract the date part and format it as "MM/DD/YYYY"
    # Using pd.to_datetime with format specification or string manipulation
    # The day name is not needed for the output date string, but helps parsing if ambiguous.
    # Since the format is consistent, we can strip the day name or parse directly.
    # pd.to_datetime can handle "Sat 12/01/2012" if we specify format or let it infer.
    # However, to be safe and deterministic:
    
    # Extract the date string part (last 10 chars usually, or split by space)
    # "Sat 12/01/2012" -> split -> ["Sat", "12/01/2012"]
    date_strs = source['CST'].str.split().str[1]
    
    # Create the 'date' column
    df = source.copy()
    df['date'] = date_strs
    
    # 2. Define the mapping from source time columns to target time columns
    # Source: 1:00, 2:00, ..., 12:00, 13:00, ..., 24:00:00
    # Target: 1:00 AM, ..., 11:00 AM, 12:00 AM, 1:00 PM, ..., 12:00 PM
    
    # Mapping logic:
    # 1-11 -> 1:00 AM - 11:00 AM
    # 12 -> 12:00 PM
    # 13-23 -> 1:00 PM - 11:00 PM
    # 24 -> 12:00 AM
    
    rename_map = {}
    
    # 1:00 to 11:00 -> 1:00 AM to 11:00 AM
    for h in range(1, 12):
        rename_map[f"{h}:00"] = f"{h}:00 AM"
        
    # 12:00 -> 12:00 PM
    rename_map["12:00"] = "12:00 PM"
    
    # 13:00 to 23:00 -> 1:00 PM to 11:00 PM
    for h in range(13, 24):
        pm_h = h - 12
        rename_map[f"{h}:00"] = f"{pm_h}:00 PM"
        
    # 24:00:00 -> 12:00 AM
    rename_map["24:00:00"] = "12:00 AM"
    
    # Apply renaming
    df = df.rename(columns=rename_map)
    
    # 3. Define the target column order
    target_columns = [
        "date",
        "1:00 AM", "2:00 AM", "3:00 AM", "4:00 AM", "5:00 AM", "6:00 AM", "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM",
        "12:00 AM",
        "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM",
        "12:00 PM"
    ]
    
    # Select and reorder columns
    result = df[target_columns]
    
    # Ensure dtypes are correct (float64 for time columns)
    # The source columns are already float64, so renaming preserves dtype.
    # The 'date' column is string.
    
    return result
