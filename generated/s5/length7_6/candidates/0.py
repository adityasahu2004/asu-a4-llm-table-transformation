import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Derive month name
    month_names = dates.dt.strftime('%B')
    
    # Derive day type: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    # Weekend if dayofweek >= 5
    day_type = dates.dt.dayofweek.apply(lambda x: "weekend" if x >= 5 else "weekday")
    
    # Prepare the output dataframe
    out = pd.DataFrame()
    out['month'] = month_names
    out['daytype'] = day_type
    
    # Rename and append hour columns
    for h in range(1, 25):
        out[f'hr{h}'] = source[h]
        
    return out
