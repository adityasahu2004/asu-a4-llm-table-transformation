import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    shifted_dates = dates - pd.Timedelta(days=182)
    
    out = pd.DataFrame(index=source.index)
    out['dt_strata'] = shifted_dates.dt.strftime('%m/%d/%Y')
    out['dow'] = shifted_dates.dt.dayofweek
    
    for h in range(1, 25):
        out[f'pct_hourly_{h:02d}00'] = source[f'Hour {h}']
        
    out['pct_hourly_2500'] = None
    
    return out.reset_index(drop=True)
