import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format
    dt = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Rename hourly columns
    for i in range(1, 25):
        src_col = f'PCT_HOURLY_{i:02d}00'
        tgt_col = f'value{i}'
        out[tgt_col] = source[src_col]
        
    return out
