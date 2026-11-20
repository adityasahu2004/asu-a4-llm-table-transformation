import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=source.index)
    dates = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    out['date'] = dates.dt.strftime('%m/%d/%Y')
    
    for h in range(1, 25):
        src_col = f'{h}:00'
        if h == 24:
            src_col = '24:00:00'
        out[f'Hour {h}'] = source[src_col]
        
    return out.reset_index(drop=True)
