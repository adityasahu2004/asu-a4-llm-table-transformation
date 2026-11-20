import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date string to datetime
    dt = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Create the target 'cst' column with the same format
    out = pd.DataFrame()
    out['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # Map source hourly columns to target hourly columns
    # Source has '1:00'...'23:00' and '24:00:00'
    # Target has '1:00'...'24:00'
    
    for h in range(1, 24):
        out[f'{h}:00'] = source[f'{h}:00']
        
    # Handle the 24th hour specifically due to name difference
    out['24:00'] = source['24:00:00']
    
    # Ensure column order matches target specification
    cols = ['cst'] + [f'{h}:00' for h in range(1, 25)]
    out = out[cols]
    
    return out.reset_index(drop=True)
