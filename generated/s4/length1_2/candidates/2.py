import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=source.index)
    
    # Parse date and format as "Weekday MM/DD/YYYY"
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    out['cst'] = dates.dt.strftime('%a %m/%d/%Y')
    
    # Rename value columns to hour labels
    for h in range(1, 25):
        out[f'{h}:00'] = source[f'value{h}']
        
    return out.reset_index(drop=True)
