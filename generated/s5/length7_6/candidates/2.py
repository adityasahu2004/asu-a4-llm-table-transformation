import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Derive month name
    out['month'] = dates.dt.strftime('%B')
    
    # Derive daytype: weekday vs weekend
    # dayofweek: 0=Mon, ..., 5=Sat, 6=Sun
    out['daytype'] = dates.dt.dayofweek.apply(lambda x: 'weekend' if x >= 5 else 'weekday')
    
    # Rename hour columns 1-24 to hr1-hr24
    for h in range(1, 25):
        out[f'hr{h}'] = source[str(h)]
        
    return out.reset_index(drop=True)
