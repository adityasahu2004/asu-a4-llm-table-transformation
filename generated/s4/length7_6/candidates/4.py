import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Derive month name
    out['month'] = dt.dt.strftime('%B')
    
    # Derive daytype: 5=Sat, 6=Sun -> weekend, else weekday
    out['daytype'] = dt.dt.weekday.apply(lambda x: 'weekend' if x >= 5 else 'weekday')
    
    # Rename hourly columns 1-24 to hr1-hr24
    for h in range(1, 25):
        out[f'hr{h}'] = source[str(h)]
        
    return out.reset_index(drop=True)
