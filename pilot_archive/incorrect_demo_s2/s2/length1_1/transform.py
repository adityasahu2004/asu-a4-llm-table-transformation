import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    dt = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame()
    
    # Format cst column: "Fri 01/01/2016"
    out['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # Map hourly columns
    for h in range(1, 25):
        src_col = f'PCT_HOURLY_{h:02d}00'
        tgt_col = f'{h}:00'
        out[tgt_col] = source[src_col]
        
    return out
