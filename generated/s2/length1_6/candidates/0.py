import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create the output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Format the date as 'DayOfWeek MM/DD/YYYY'
    out['cst'] = dates.dt.strftime('%a %m/%d/%Y')
    
    # Map source hourly columns to target hourly columns
    for h in range(1, 25):
        out[f'{h}:00'] = source[f'Hr {h}']
        
    return out.reset_index(drop=True)
