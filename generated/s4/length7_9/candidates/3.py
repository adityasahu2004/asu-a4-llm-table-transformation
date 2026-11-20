import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Derive 'month'
    month = dates.dt.strftime('%B')
    
    # Derive 'daytype'
    # dayofweek: Monday=0, ..., Sunday=6
    dow = dates.dt.dayofweek
    daytype = dow.map(lambda x: "weekend" if x >= 5 else "weekday")
    
    # Map hourly columns
    # Source: 1:00, 2:00, ..., 23:00, 24:00:00
    # Target: hr1, hr2, ..., hr23, hr24
    
    # Build the mapping dictionary
    hour_cols = {}
    for h in range(1, 24):
        hour_cols[f'{h}:00'] = f'hr{h}'
    hour_cols['24:00:00'] = 'hr24'
    
    # Select and rename
    hourly_df = source.rename(columns=hour_cols)
    
    # Construct final dataframe
    out = pd.DataFrame()
    out['month'] = month
    out['daytype'] = daytype
    
    # Append hourly columns in order hr1 to hr24
    for h in range(1, 25):
        out[f'hr{h}'] = hourly_df[f'hr{h}']
        
    return out
