import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and shift back 6 months
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    shifted_dt = dt - pd.DateOffset(months=6)
    
    # Create output dataframe
    out = pd.DataFrame()
    out['Date'] = shifted_dt.strftime('%Y-%m-%d 00:00:00')
    
    # Rename and copy hourly columns
    for h in range(1, 25):
        src_col = f'Hour {h}'
        tgt_col = f'Hr {h}'
        out[tgt_col] = source[src_col]
        
    return out
