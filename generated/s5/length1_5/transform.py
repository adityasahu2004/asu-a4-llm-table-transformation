import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and shift by -6 months
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    shifted_dates = dates - pd.DateOffset(months=6)
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Format cst column
    out['cst'] = shifted_dates.dt.strftime('%a %m/%d/%Y')
    
    # Rename and copy hourly columns
    for h in range(1, 25):
        src_col = f'Hour {h}'
        tgt_col = f'{h}:00'
        
        # Check if source column exists to avoid errors if schema varies slightly
        if src_col in source.columns:
            out[tgt_col] = source[src_col].astype(float)
            
            # Enforce int64 for columns 9:00 through 16:00 as per target schema
            if 9 <= h <= 16:
                out[tgt_col] = out[tgt_col].astype('Int64') # Use nullable int or standard int if no nulls
                
    return out.reset_index(drop=True)
