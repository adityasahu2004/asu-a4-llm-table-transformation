import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Process the Date column
    # Source format: "Thu MM/DD/YYYY"
    # Target format: "MM/DD/YYYY"
    # We can simply slice the string from index 4 to remove the day name and space.
    df = source.copy()
    df['date'] = df['Date'].str[4:]
    
    # 2. Define the mapping from source hour columns to target hour columns
    # Source columns: "1:00" to "23:00", "24:00:00"
    # Target columns: "1:00 AM" to "11:00 AM", "12:00 AM", "1:00 PM" to "11:00 PM", "12:00 PM"
    
    # Mapping logic based on 24h to 12h conversion:
    # 1-11 -> 1:00 AM - 11:00 AM
    # 12 -> 12:00 PM (Noon)
    # 13-23 -> 1:00 PM - 11:00 PM
    # 24 -> 12:00 AM (Midnight)
    
    col_mapping = {}
    
    # 1:00 to 11:00 -> 1:00 AM to 11:00 AM
    for h in range(1, 12):
        src_col = f"{h}:00"
        tgt_col = f"{h}:00 AM"
        col_mapping[src_col] = tgt_col
        
    # 12:00 -> 12:00 PM
    col_mapping["12:00"] = "12:00 PM"
    
    # 13:00 to 23:00 -> 1:00 PM to 11:00 PM
    for h in range(13, 24):
        src_col = f"{h}:00"
        tgt_h = h - 12
        tgt_col = f"{tgt_h}:00 PM"
        col_mapping[src_col] = tgt_col
        
    # 24:00:00 -> 12:00 AM
    col_mapping["24:00:00"] = "12:00 AM"
    
    # 3. Rename the columns
    df = df.rename(columns=col_mapping)
    
    # 4. Define the target column order
    target_columns = [
        "date",
        "1:00 AM", "2:00 AM", "3:00 AM", "4:00 AM", "5:00 AM", "6:00 AM", "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM",
        "12:00 AM",
        "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM",
        "12:00 PM"
    ]
    
    # 5. Select and reorder columns
    # Ensure all target columns exist in the dataframe
    result = df[target_columns]
    
    return result
