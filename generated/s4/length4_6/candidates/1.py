import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Format the date as required: YYYY-MM-DD HH:MM:SS
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Mapping for hours 1-24 to the target 12-hour AM/PM format
    # Source Hr 1 -> 1:00 AM, ..., Hr 12 -> 12:00 AM, Hr 13 -> 1:00 PM, ..., Hr 24 -> 12:00 PM
    hour_map = {}
    for h in range(1, 25):
        if h <= 12:
            # 1-11: 1:00 AM - 11:00 AM
            # 12: 12:00 AM
            if h == 12:
                label = "12:00 AM"
            else:
                label = f"{h}:00 AM"
        else:
            # 13-23: 1:00 PM - 11:00 PM
            # 24: 12:00 PM
            if h == 24:
                label = "12:00 PM"
            else:
                label = f"{h-12}:00 PM"
        hour_map[f'Hr {h}'] = label
        
    # Rename the hour columns and select them
    # We assume source columns are strictly 'Hr 1' to 'Hr 24' based on schema
    hour_cols = [f'Hr {h}' for h in range(1, 25)]
    df_hours = source[hour_cols].rename(columns=hour_map)
    
    # Combine date and hours
    out = pd.concat([out, df_hours], axis=1)
    
    return out.reset_index(drop=True)
