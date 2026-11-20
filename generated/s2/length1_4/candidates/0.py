import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create the target 'cst' column
    out = pd.DataFrame()
    out['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # Map integer hour columns to 'H:00' format
    for h in range(1, 25):
        out[f'{h}:00'] = source[str(h)]
        
    return out
