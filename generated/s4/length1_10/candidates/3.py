import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    source = source.copy()
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # Filter for cooling season (84.0)
    # Rows with 73.0 or NaN are ignored
    cooling_active = source[source['zone_016_cooling_sp'] == 84.0]
    
    if cooling_active.empty:
        # Return empty dataframe with correct schema if no cooling data
        return pd.DataFrame(columns=['cst'] + [f'{h}:00' for h in range(1, 25)])

    # Extract date and hour
    cooling_active['date_only'] = cooling_active['dt'].dt.normalize()
    cooling_active['hour'] = cooling_active['dt'].dt.hour + 1 # 0-23 -> 1-24
    
    # Get unique dates
    unique_dates = sorted(cooling_active['date_only'].unique())
    
    records = []
    for date in unique_dates:
        day_data = cooling_active[cooling_active['date_only'] == date]
        active_hours = day_data['hour'].unique()
        
        row = {'cst': date.strftime('%a %m/%d/%Y')}
        for h in range(1, 25):
            if h in active_hours:
                row[f'{h}:00'] = 876.0
            else:
                row[f'{h}:00'] = 0.0
        records.append(row)
        
    result = pd.DataFrame(records)
    
    # Ensure column order
    cols = ['cst'] + [f'{h}:00' for h in range(1, 25)]
    result = result[cols]
    
    return result.reset_index(drop=True)
