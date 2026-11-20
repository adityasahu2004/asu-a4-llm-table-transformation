import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=source.index)
    
    # Parse date and format as MM/DD/YYYY
    dt = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Map the 24 hourly columns to value1...value24
    for h in range(1, 25):
        src_col = f'PCT_HOURLY_{h:02d}00'
        tgt_col = f'value{h}'
        out[tgt_col] = source[src_col]
        
    return out.reset_index(drop=True)
