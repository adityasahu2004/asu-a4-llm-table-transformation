import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source hourly load data into a formatted daily/weekly view.
    """
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse the date column
    # Source format: MM/DD/YYYY (e.g., "7/3/2011")
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Format the 'cst' column
    # Target format: "Day MM/DD/YYYY" (e.g., "Sat 01/01/2011")
    # Day abbreviation (3 chars), Month (zero-padded), Day (zero-padded), Year
    df['cst'] = df['date_parsed'].dt.strftime('%a %m/%d/%Y')
    
    # 3. Rename value columns from 'value1'...'value24' to '1:00'...'24:00'
    rename_mapping = {}
    for i in range(1, 25):
        rename_mapping[f'value{i}'] = f'{i}:00'
    
    df = df.rename(columns=rename_mapping)
    
    # 4. Select and order the columns
    # Target columns: 'cst', '1:00', '2:00', ..., '24:00'
    time_cols = [f'{i}:00' for i in range(1, 25)]
    final_cols = ['cst'] + time_cols
    
    # Ensure we only select columns that exist and are in the correct order
    # The source has value1-24, which are now renamed.
    result = df[final_cols].reset_index(drop=True)
    
    return result
