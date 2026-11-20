import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    dt = pd.to_datetime(source['Date'])
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # dt_strata: Format as M/D/YYYY (no leading zeros based on sample)
    # Since source 'Date' is already in this format and matches target, we can just copy it.
    # However, to be safe against sorting or other issues, we construct it.
    # But simple copy is safest if format is identical.
    out['dt_strata'] = source['Date']
    
    # dow: Sun=0, Mon=1, ..., Sat=6
    # pandas dayofweek: Mon=0, ..., Sun=6
    # Formula: (dayofweek + 1) % 7
    out['dow'] = (dt.dt.dayofweek + 1) % 7
    
    # Rename hourly columns
    for h in range(1, 25):
        src_col = f'Hr {h}'
        tgt_col = f'pct_hourly_{h:02d}00'
        out[tgt_col] = source[src_col]
        
    # Add 25th hour column with 0
    out['pct_hourly_2500'] = 0
    
    return out.reset_index(drop=True)
