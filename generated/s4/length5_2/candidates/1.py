import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the CST column to datetime
    # Format is "DayOfWeek MM/DD/YYYY", e.g., "Sat 12/01/2012"
    dt = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    # Create the target 'date' column formatted as MM/DD/YYYY
    out = pd.DataFrame()
    out['date'] = dt.strftime('%m/%d/%Y')
    
    # Map source hourly columns to target value columns
    # Source cols: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target cols: 'value1', 'value2', ..., 'value24'
    
    for i in range(1, 25):
        if i < 24:
            src_col = f"{i}:00"
        else:
            src_col = "24:00:00"
        
        tgt_col = f"value{i}"
        out[tgt_col] = source[src_col].astype(float)
        
    return out.reset_index(drop=True)
