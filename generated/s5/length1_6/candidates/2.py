import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format to 'cst'
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    out['cst'] = dates.dt.strftime('%a %m/%d/%Y')
    
    # Rename hourly columns
    for h in range(1, 25):
        out[f'{h}:00'] = source[f'Hr {h}']
        
    return out.reset_index(drop=True)
