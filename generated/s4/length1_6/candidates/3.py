import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date string to datetime to extract weekday and format correctly
    # Format observed in source: "1/1/2014" -> %m/%d/%Y
    # Format observed in target: "Wed 01/01/2014" -> %a %m/%d/%Y
    dt_series = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create the 'cst' column
    cst_col = dt_series.dt.strftime('%a %m/%d/%Y')
    
    # Initialize the result dataframe
    result = pd.DataFrame(index=source.index)
    result['cst'] = cst_col
    
    # Map the 24 hourly columns
    # Source: "Hr 1", "Hr 2", ..., "Hr 24"
    # Target: "1:00", "2:00", ..., "24:00"
    for h in range(1, 25):
        src_col = f'Hr {h}'
        tgt_col = f'{h}:00'
        result[tgt_col] = source[src_col]
        
    return result.reset_index(drop=True)
