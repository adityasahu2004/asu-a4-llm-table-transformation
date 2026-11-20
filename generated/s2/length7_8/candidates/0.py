import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    out['month'] = dates.dt.strftime('%B').str.ljust(10)
    out['daytype'] = dates.dt.dayofweek.apply(lambda d: 'weekend' if d >= 5 else 'weekday')
    for h in range(1, 25):
        out[f'hr{h}'] = source[f'Hr {h}']
    return out.reset_index(drop=True)
