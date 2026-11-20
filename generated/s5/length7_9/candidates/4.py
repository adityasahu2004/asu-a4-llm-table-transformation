import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format in source: "Thu 10/01/2009" -> %a %m/%d/%Y
    dates = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Derive month name
    out_month = dates.dt.strftime('%B')
    
    # Derive daytype
    # dayofweek: 0=Monday, ..., 5=Saturday, 6=Sunday
    is_weekend = dates.dt.dayofweek.isin([5, 6])
    out_daytype = np.where(is_weekend, "weekend", "weekday")
    
    # Build the result DataFrame
    result = pd.DataFrame(index=source.index)
    result['month'] = out_month
    result['daytype'] = out_daytype
    
    # Map hour columns
    # Source columns: "1:00" ... "23:00", "24:00:00"
    # Target columns: "hr1" ... "hr24"
    for h in range(1, 24):
        result[f'hr{h}'] = source[f'{h}:00']
    
    # Handle the 24th hour specifically due to naming difference
    result['hr24'] = source['24:00:00']
    
    # Select final columns in order
    cols = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    result = result[cols]
    
    return result.reset_index(drop=True)
