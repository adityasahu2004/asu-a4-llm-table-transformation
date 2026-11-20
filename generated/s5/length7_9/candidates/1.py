import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format is e.g., "Thu 10/01/2009" -> %a %m/%d/%Y
    dt = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Extract month name
    month = dt.dt.strftime('%B')
    
    # Determine day type
    # dayofweek: Monday=0 ... Saturday=5, Sunday=6
    day_type = np.where(dt.dt.dayofweek >= 5, 'weekend', 'weekday')
    
    # Map hourly columns
    # Source: 1:00 ... 23:00, 24:00:00
    # Target: hr1 ... hr23, hr24
    
    out = pd.DataFrame(index=source.index)
    out['month'] = month
    out['daytype'] = day_type
    
    for h in range(1, 24):
        out[f'hr{h}'] = source[f'{h}:00']
        
    # Handle the 24th hour specifically as it has seconds in source name
    out['hr24'] = source['24:00:00']
    
    # Ensure column order matches target schema
    cols = ['month', 'daytype'] + [f'hr{h}' for h in range(1, 25)]
    return out[cols].reset_index(drop=True)
