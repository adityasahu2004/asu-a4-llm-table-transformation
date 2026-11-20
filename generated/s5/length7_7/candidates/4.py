import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Construct output dataframe
    out = pd.DataFrame()
    
    # Month name
    out['month'] = dates.dt.strftime('%B')
    
    # Day type: 5=Sat, 6=Sun in pandas dayofweek (Mon=0)
    out['daytype'] = dates.dt.dayofweek.map(
        lambda d: 'weekend' if d >= 5 else 'weekday'
    )
    
    # Rename hourly columns
    for h in range(1, 25):
        out[f'hr{h}'] = source[f'Hour {h}']
        
    return out
