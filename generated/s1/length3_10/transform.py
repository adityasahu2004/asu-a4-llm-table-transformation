import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame by:
    1. Parsing the 'Date' column from "Thu MM/DD/YYYY" to "MM/DD/YYYY".
    2. Renaming hour columns from "H:00" (or "24:00:00") to "Hour H".
    3. Dropping the 'Segment' column.
    4. Reordering columns to match the target schema.
    """
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Process Date Column
    # Source format: "Thu 10/01/2009"
    # Target format: "10/01/2009"
    # We can parse using pd.to_datetime and then format, or simply split.
    # Using pd.to_datetime is robust.
    # Format string for input: "%a %m/%d/%Y"
    # Format string for output: "%m/%d/%Y"
    
    df['date'] = pd.to_datetime(df['Date'], format="%a %m/%d/%Y").dt.strftime("%m/%d/%Y")
    
    # 2. Rename Hour Columns
    # Source columns: "1:00", "2:00", ..., "23:00", "24:00:00"
    # Target columns: "Hour 1", "Hour 2", ..., "Hour 23", "Hour 24"
    
    rename_map = {}
    for col in df.columns:
        if col == 'Date' or col == 'Segment' or col == 'date':
            continue
        
        # Check if it's an hour column
        # Pattern: "H:00" or "24:00:00"
        if col.endswith(':00') or col.endswith(':00:00'):
            # Extract the hour number
            # For "1:00", split by ':' -> ["1", "00"]
            # For "24:00:00", split by ':' -> ["24", "00", "00"]
            hour_str = col.split(':')[0]
            try:
                hour_num = int(hour_str)
                rename_map[col] = f"Hour {hour_num}"
            except ValueError:
                pass # Skip if not a valid hour column
    
    df.rename(columns=rename_map, inplace=True)
    
    # 3. Select and Order Columns
    # Target columns: date, Hour 1, ..., Hour 24
    target_cols = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # Ensure all target columns exist (they should based on schema)
    df = df[target_cols]
    
    return df
