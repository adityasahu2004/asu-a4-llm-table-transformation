import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=source.index)
    
    # Parse date and format as MM/DD/YYYY
    dates = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    out['date'] = dates.dt.strftime('%m/%d/%Y')
    
    # Rename hourly columns
    for h in range(1, 25):
        src_col = f'{h}:00' if h < 24 else '24:00:00'
        tgt_col = f'Hour {h}'
        out[tgt_col] = source[src_col]
        
    return out.reset_index(drop=True)
