import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format the date for the 'cst' column
    cst_formatted = dt.strftime('%a %m/%d/%Y')
    
    # Create mapping for value columns to target hour columns
    # Source: value1...value24 -> Target: 1:00...24:00
    rename_map = {}
    for i in range(1, 25):
        rename_map[f'value{i}'] = f'{i}:00'
        
    # Select and rename the relevant columns
    # We select the date first, then the value columns in order
    result = pd.DataFrame()
    result['cst'] = cst_formatted
    
    for i in range(1, 25):
        result[f'{i}:00'] = source[f'value{i}']
        
    return result.reset_index(drop=True)
