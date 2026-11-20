import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=source.index)
    
    # Parse and format date
    dt = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    out['Date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Rename hourly columns
    for h in range(1, 25):
        src_col = f'PCT_HOURLY_{h:02d}00'
        tgt_col = f'Hr {h}'
        out[tgt_col] = source[src_col]
        
    return out.reset_index(drop=True)
