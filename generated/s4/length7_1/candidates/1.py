import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    dates = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    out['month'] = dates.dt.strftime('%B').str.pad(10, side='right')
    out['daytype'] = dates.dt.dayofweek.map(lambda x: 'weekend' if x >= 5 else 'weekday')
    for h in range(1, 25):
        src_col = f'{h}:00' if h < 24 else '24:00:00'
        out[f'hr{h}'] = source[src_col]
    return out.reset_index(drop=True)
