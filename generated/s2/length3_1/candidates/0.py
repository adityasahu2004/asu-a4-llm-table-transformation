import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format
    dt = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Map hourly columns
    for h in range(1, 25):
        src_col = f'PCT_HOURLY_{h:02d}00'
        tgt_col = f'Hour {h}'
        out[tgt_col] = source[src_col]
        
    return out
