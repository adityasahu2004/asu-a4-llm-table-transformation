import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    dt = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    out['month'] = dt.dt.strftime('%B').str.ljust(10)
    out['daytype'] = dt.dt.dayofweek.apply(lambda d: 'weekend' if d >= 5 else 'weekday')
    for h in range(1,25):
        src_name = f'{h}:00' if h < 24 else '24:00:00'
        out[f'hr{h}'] = pd.to_numeric(source[src_name], errors='coerce')
    return out.reset_index(drop=True)
