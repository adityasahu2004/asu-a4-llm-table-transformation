import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    out['dt_strata'] = dates.dt.strftime('%-m/%-d/%Y')
    out['dow'] = dates.dt.dayofweek
    for h in range(1, 25):
        out[f'pct_hourly_{h:02d}00'] = source[f'Hour {h}']
    out['pct_hourly_2500'] = float('nan')
    return out.reset_index(drop=True)
