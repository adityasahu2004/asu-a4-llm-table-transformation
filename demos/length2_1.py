import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    dates = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    out['dt_strata'] = dates.dt.strftime('%m/%d/%Y')
    out['dow'] = dates.dt.dayofweek + 1
    for h in range(1,25):
        name = f'{h}:00' if h < 24 else '24:00:00'
        out[f'pct_hourly_{h:02d}00'] = pd.to_numeric(source[name], errors='coerce')
    out['pct_hourly_2500'] = 0
    return out.reset_index(drop=True)
