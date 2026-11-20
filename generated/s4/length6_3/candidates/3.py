import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format to ISO string with time component
    dt_series = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create the output dataframe
    out = pd.DataFrame(index=source.index)
    out['Date'] = dt_series.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Rename value1..value24 to Hr 1..Hr 24
    for i in range(1, 25):
        out[f'Hr {i}'] = source[f'value{i}']
        
    return out.reset_index(drop=True)
