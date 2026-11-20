import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse CST to datetime to extract date
    # Format is "DayOfWeek MM/DD/YYYY"
    dt_series = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame()
    out['date'] = dt_series.dt.strftime('%m/%d/%Y')
    
    # Map source hour columns to target value columns
    # Source: 1:00, 2:00, ..., 23:00, 24:00:00
    # Target: value1, value2, ..., value23, value24
    
    # Handle hours 1-23
    for h in range(1, 24):
        out[f'value{h}'] = source[f'{h}:00']
        
    # Handle hour 24 (source is "24:00:00")
    out['value24'] = source['24:00:00']
    
    return out
