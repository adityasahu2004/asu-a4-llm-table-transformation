import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    out = source.copy()
    
    # Parse date and shift back 6 years
    dates = pd.to_datetime(out['Date'], format='%a %m/%d/%Y')
    shifted_dates = dates - pd.DateOffset(years=6)
    
    # Format new date string
    out['cst'] = shifted_dates.dt.strftime('%a %m/%d/%Y')
    
    # Rename columns
    rename_map = {
        '24:00:00': '24:00'
    }
    
    # Select and rename columns
    cols = ['cst'] + [f'{h}:00' if h < 24 else '24:00:00' for h in range(1, 25)]
    
    # Construct final dataframe
    result = pd.DataFrame(index=out.index)
    result['cst'] = out['cst']
    
    for h in range(1, 24):
        result[f'{h}:00'] = out[f'{h}:00']
    result['24:00'] = out['24:00:00']
    
    return result.reset_index(drop=True)
