import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format as MM/DD/YYYY
    dates = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    out = pd.DataFrame()
    out['Date'] = dates.dt.strftime('%m/%d/%Y')
    
    # Rename hourly columns
    for h in range(1, 25):
        src_col = f'PCT_HOURLY_{h:02d}00'
        tgt_col = f'Hr {h}'
        out[tgt_col] = source[src_col]
        
    return out
