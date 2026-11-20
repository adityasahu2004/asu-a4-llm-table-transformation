import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Derive target date: subtract 6 months and format as "Dow MM/DD/YYYY"
    # Using pd.DateOffset to handle month arithmetic correctly
    target_dates = dates - pd.DateOffset(months=6)
    
    out = pd.DataFrame(index=source.index)
    out['cst'] = target_dates.dt.strftime('%a %m/%d/%Y')
    
    # Rename columns 1..24 to 1:00..24:00
    for h in range(1, 25):
        out[f'{h}:00'] = source[str(h)]
        
    return out.reset_index(drop=True)
