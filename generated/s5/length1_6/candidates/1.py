import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format to 'cst'
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    out = pd.DataFrame()
    out['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # Map Hr 1..24 to 1:00..24:00
    for h in range(1, 25):
        out[f'{h}:00'] = source[f'Hr {h}']
        
    return out.reset_index(drop=True)
