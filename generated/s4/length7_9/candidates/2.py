import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    dates = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    out['month'] = dates.dt.strftime('%B')
    out['daytype'] = dates.dt.dayofweek.map({0:'weekday',1:'weekday',2:'weekday',3:'weekday',4:'weekday',5:'weekend',6:'weekend'})
    for h in range(1,25):
        src_col = f'{h}:00' if h < 24 else '24:00:00'
        out[f'hr{h}'] = source[src_col]
    return out.reset_index(drop=True)
