import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Identify the hourly columns from the source.
    # Source columns are "1" through "24".
    hour_cols = [str(i) for i in range(1, 25)]
    
    # Create a mapping for renaming hourly columns to "Hr X"
    rename_map = {str(i): f"Hr {i}" for i in range(1, 25)}
    
    # Select the Date column and the hourly columns
    result = source[["Date"] + hour_cols].copy()
    
    # Rename the hourly columns
    result = result.rename(columns=rename_map)
    
    # Reset index to ensure a clean 0-based integer index
    result = result.reset_index(drop=True)
    
    return result
