import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates from format "Thu 10/01/2009"
    dates = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    out = pd.DataFrame(index=source.index)
    
    # Extract month name
    out['month'] = dates.dt.strftime('%B')
    
    # Determine daytype: weekday (Mon-Fri) or weekend (Sat-Sun)
    # dayofweek: 0=Mon, ..., 4=Fri, 5=Sat, 6=Sun
    out['daytype'] = dates.dt.dayofweek.apply(lambda d: 'weekend' if d >= 5 else 'weekday')
    
    # Rename hourly columns
    for h in range(1, 25):
        src_col = f'{h}:00' if h < 24 else '24:00:00'
        out[f'hr{h}'] = source[src_col]
        
    return out.reset_index(drop=True)
