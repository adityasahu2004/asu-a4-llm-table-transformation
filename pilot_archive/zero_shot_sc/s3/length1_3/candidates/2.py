import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame by:
    1. Parsing the 'date' column and shifting it back by 6 months.
    2. Formatting the date as 'DayOfWeek MM/DD/YYYY'.
    3. Renaming the hourly columns from 12-hour AM/PM format to 24-hour format (1:00 to 24:00).
    """
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse and Shift Date
    # Parse the date string (M/D/YYYY format)
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # Shift date back by 6 months
    df['date'] = df['date'] - pd.DateOffset(months=6)
    
    # Format date as "DayOfWeek MM/DD/YYYY" (e.g., "Wed 01/01/2014")
    # %a gives abbreviated weekday name (Wed)
    df['cst'] = df['date'].dt.strftime('%a %m/%d/%Y')
    
    # 2. Rename Columns
    # Map source column names to target column names
    # Source: "1:00 AM", "2:00 AM", ..., "11:00 AM", "12:00 PM", "1:00 PM", ..., "11:00 PM", "12:00 AM"
    # Target: "1:00", "2:00", ..., "11:00", "12:00", "13:00", ..., "23:00", "24:00"
    
    col_mapping = {}
    
    # Handle AM columns (1:00 AM to 11:00 AM)
    for h in range(1, 12):
        src_col = f"{h}:00 AM"
        tgt_col = f"{h}:00"
        if src_col in df.columns:
            col_mapping[src_col] = tgt_col
            
    # Handle PM columns (12:00 PM to 11:00 PM)
    # 12:00 PM -> 12:00
    # 1:00 PM -> 13:00
    # ...
    # 11:00 PM -> 23:00
    for h in range(12, 24):
        # Source hour in 12-hour format
        if h == 12:
            src_h = 12
            period = "PM"
        else:
            src_h = h - 12
            period = "PM"
        
        src_col = f"{src_h}:00 {period}"
        tgt_col = f"{h}:00"
        if src_col in df.columns:
            col_mapping[src_col] = tgt_col
            
    # Handle 12:00 AM -> 24:00
    src_col = "12:00 AM"
    tgt_col = "24:00"
    if src_col in df.columns:
        col_mapping[src_col] = tgt_col
        
    # Rename columns
    df = df.rename(columns=col_mapping)
    
    # 3. Select and Order Columns
    # Target columns: 'cst', '1:00', ..., '24:00'
    target_cols = ['cst'] + [f"{h}:00" for h in range(1, 25)]
    
    # Ensure all target columns exist in the dataframe (they should based on schema)
    # Filter to only include target columns
    result = df[target_cols].copy()
    
    # Drop the original date column if it's still there (it is, but not in target_cols)
    # The selection above handles this.
    
    # Sort by date to ensure consistent order (though input is likely sorted)
    # We need to sort by the actual date, not the string. 
    # We can use the original datetime column for sorting if we kept it, 
    # but we overwrote it. Let's parse the string back or just assume order is preserved.
    # To be safe, let's parse the 'cst' column back to datetime for sorting.
    # Format is "%a %m/%d/%Y"
    result['_sort_date'] = pd.to_datetime(result['cst'], format='%a %m/%d/%Y')
    result = result.sort_values('_sort_date')
    result = result.drop(columns=['_sort_date'])
    
    return result
