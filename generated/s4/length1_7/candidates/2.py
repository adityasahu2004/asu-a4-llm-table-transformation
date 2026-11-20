import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    dates = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    shifted_dates = dates - pd.DateOffset(years=7)
    
    out = pd.DataFrame(index=source.index)
    out['cst'] = shifted_dates.dt.strftime('%a %m/%d/%Y')
    
    for h in range(1, 24):
        out[f'{h}:00'] = source[f'{h}:00']
    
    out['24:00'] = source['24:00:00']
    
    return out.reset_index(drop=True)
