import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    dates = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    out = pd.DataFrame(index=source.index)
    
    # Month name left-padded to 11 characters
    out['month'] = dates.dt.strftime('%B').str.ljust(11)
    
    # Day type: weekday or weekend
    dow = dates.dt.dayofweek  # Monday=0, Sunday=6
    out['daytype'] = dow.apply(lambda d: 'weekday' if d < 5 else 'weekend')
    
    # Rename hourly columns
    for h in range(1, 25):
        src_col = f'{h}:00' if h < 24 else '24:00:00'
        out[f'hr{h}'] = pd.to_numeric(source[src_col], errors='coerce')
        
    return out.reset_index(drop=True)
