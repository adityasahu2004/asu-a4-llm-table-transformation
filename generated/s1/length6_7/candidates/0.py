import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame by:
    1. Dropping the 'Segment' column.
    2. Renaming hourly columns from 'H:MM' format to 'Hr H' format.
    3. Reordering columns to match the target schema.
    """
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Define the mapping from source column names to target column names
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hr 1', 'Hr 2', ..., 'Hr 23', 'Hr 24'
    
    rename_map = {}
    for hour in range(1, 24):
        rename_map[f"{hour}:00"] = f"Hr {hour}"
    rename_map["24:00:00"] = "Hr 24"
    
    # Apply renaming
    df = df.rename(columns=rename_map)
    
    # Drop the 'Segment' column
    if 'Segment' in df.columns:
        df = df.drop(columns=['Segment'])
    
    # Define the target column order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # Select and reorder columns
    df = df[target_columns]
    
    return df
