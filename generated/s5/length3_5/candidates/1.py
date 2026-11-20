import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the source date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format to the target string pattern
    out = pd.DataFrame()
    out['date'] = dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Rename value1..value24 to Hour 1..Hour 24
    for i in range(1, 25):
        out[f'Hour {i}'] = source[f'value{i}']
        
    return out.reset_index(drop=True)
