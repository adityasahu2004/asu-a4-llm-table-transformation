import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame by:
    1. Parsing the 'CST' date column.
    2. Sorting by date.
    3. Formatting the date as 'MM/DD/YYYY'.
    4. Renaming hour-based columns to 'value1'...'value24'.
    5. Returning the DataFrame with columns ['date', 'value1', ..., 'value24'].
    """
    df = source.copy()
    
    # Parse CST column: "Day MM/DD/YYYY"
    # Example: "Sat 12/01/2012"
    df['parsed_date'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    
    # Sort by date
    df = df.sort_values('parsed_date').reset_index(drop=True)
    
    # Format date column
    df['date'] = df['parsed_date'].dt.strftime('%m/%d/%Y')
    
    # Create mapping for value columns
    # Source: '1:00'...'23:00', '24:00:00'
    # Target: 'value1'...'value24'
    col_map = {}
    for i in range(1, 24):
        col_map[f"{i}:00"] = f"value{i}"
    col_map["24:00:00"] = "value24"
    
    # Rename columns
    df = df.rename(columns=col_map)
    
    # Define final column order
    value_cols = [f"value{i}" for i in range(1, 25)]
    final_cols = ['date'] + value_cols
    
    # Drop helper columns and select final columns
    df = df.drop(columns=['CST', 'parsed_date'])
    df = df[final_cols]
    
    return df
