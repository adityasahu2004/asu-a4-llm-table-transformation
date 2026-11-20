import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Process the Date column
    # Source CST format: "Day MM/DD/YYYY" (e.g., "Sat 12/01/2012")
    # Target Date format: "MM/DD/YYYY" (e.g., "12/01/2012")
    # We extract the date part by splitting on space and taking the last element.
    source['Date'] = source['CST'].str.split().str[-1]
    
    # 2. Rename the hour columns
    # Source columns: "1:00", "2:00", ..., "23:00", "24:00:00"
    # Target columns: "Hr 1", "Hr 2", ..., "Hr 23", "Hr 24"
    
    rename_map = {}
    for col in source.columns:
        if col == 'CST':
            continue
        # Extract the hour number from the column name
        # "1:00" -> 1
        # "24:00:00" -> 24
        hour_str = col.split(':')[0]
        rename_map[col] = f'Hr {hour_str}'
        
    source = source.rename(columns=rename_map)
    
    # 3. Select and order the columns
    # Target order: Date, Hr 1, Hr 2, ..., Hr 24
    target_cols = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    result = source[target_cols]
    
    # Ensure numeric types for hour columns
    for col in target_cols[1:]:
        result[col] = pd.to_numeric(result[col], errors='coerce')
        
    return result
