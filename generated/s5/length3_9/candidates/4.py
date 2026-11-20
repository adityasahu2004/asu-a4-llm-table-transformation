import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse and format the date
    # Source format is observed as "1/1/2014" (m/d/Y)
    # Target format is observed as "01/01/2014" (mm/dd/yyyy)
    parsed_dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    date_formatted = parsed_dates.dt.strftime('%m/%d/%Y')
    
    # 2. Create the output DataFrame with the date column
    out = pd.DataFrame({
        'date': date_formatted
    }, index=source.index)
    
    # 3. Rename and project the hourly columns
    # Source: "Hr 1" ... "Hr 24"
    # Target: "Hour 1" ... "Hour 24"
    for h in range(1, 25):
        src_col = f'Hr {h}'
        tgt_col = f'Hour {h}'
        if src_col in source.columns:
            out[tgt_col] = source[src_col]
            
    # 4. Reset index to ensure clean integer index
    return out.reset_index(drop=True)
