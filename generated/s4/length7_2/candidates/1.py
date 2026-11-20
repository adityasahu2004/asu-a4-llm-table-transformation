import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    dates = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    out['month'] = dates.dt.strftime('%B').str.ljust(10)
    out['daytype'] = 'weekday'
    for h in range(1, 25):
        out[f'hr{h}'] = source[f'PCT_HOURLY_{h:02d}00']
    return out.reset_index(drop=True)
