import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format to YYYY-MM-DD 00:00:00
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    out = pd.DataFrame()
    out['date'] = dt.strftime('%Y-%m-%d 00:00:00')
    
    # Rename Hour columns to value columns
    for h in range(1, 25):
        out[f'value{h}'] = source[f'Hour {h}']
        
    return out.reset_index(drop=True)
