import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Derive month name
    month_names = dates.dt.strftime('%B')
    
    # Derive daytype: 5=Sat, 6=Sun are weekends
    day_of_week = dates.dt.dayofweek
    daytype = day_of_week.apply(lambda d: "weekend" if d >= 5 else "weekday")
    
    # Build the result dataframe
    out = pd.DataFrame()
    out['month'] = month_names
    out['daytype'] = daytype
    
    # Rename hour columns 1-24 to hr1-hr24
    for h in range(1, 25):
        out[f'hr{h}'] = source[str(h)]
        
    # Sort by month then daytype to match target sample order
    # Target sample shows January weekday, January weekday, February weekend, February weekday...
    # Alphabetical sort: January < February... and weekday < weekend
    out = out.sort_values(by=['month', 'daytype']).reset_index(drop=True)
    
    return out
