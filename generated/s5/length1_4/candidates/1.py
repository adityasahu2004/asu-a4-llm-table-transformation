import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame()
    out['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # Rename hour columns
    for h in range(1, 25):
        out[f'{h}:00'] = source[h]
        
    return out
