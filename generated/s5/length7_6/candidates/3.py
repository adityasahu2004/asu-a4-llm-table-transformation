import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    out['month'] = dates.dt.strftime('%B')
    out['daytype'] = dates.dt.dayofweek.map(lambda d: 'weekday' if d < 5 else 'weekend')
    for h in range(1, 25):
        out[f'hr{h}'] = source[str(h)]
    return out.reset_index(drop=True)
