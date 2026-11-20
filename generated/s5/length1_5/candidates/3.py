import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Subtract 183 days
    shifted_dates = dates - pd.Timedelta(days=183)
    
    # Format the new date column
    cst_formatted = shifted_dates.dt.strftime('%a %m/%d/%Y')
    
    # Create the output dataframe
    out = pd.DataFrame()
    out['cst'] = cst_formatted
    
    # Rename Hour columns to HH:00 format
    for h in range(1, 25):
        out[f'{h}:00'] = source[f'Hour {h}']
        
    return out
