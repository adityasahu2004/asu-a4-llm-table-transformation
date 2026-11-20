import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date string 'Thu 10/01/2009' to datetime
    # Format is '%a %m/%d/%Y'
    dates = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Create the output dataframe with the formatted date string
    out = pd.DataFrame(index=source.index)
    out['Date'] = dates.dt.strftime('%a %m/%d/%Y')
    
    # Map source hour columns to target hour columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'Hr 1', 'Hr 2', ..., 'Hr 23', 'Hr 24'
    
    for h in range(1, 24):
        out[f'Hr {h}'] = source[f'{h}:00']
    
    # Handle the 24th hour specifically due to different source name '24:00:00'
    out['Hr 24'] = source['24:00:00']
    
    return out.reset_index(drop=True)
