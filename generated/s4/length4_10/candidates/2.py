import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Pivot
    pivoted = df.pivot_table(index='date_only', columns='hour', values='zone_016_cooling_sp', aggfunc='first')
    
    # Rename hours to target format
    hour_names = []
    for h in range(24):
        if h == 0:
            hour_names.append("12:00 AM")
        elif h < 12:
            hour_names.append(f"{h}:00 AM")
        elif h == 12:
            hour_names.append("12:00 PM")
        else:
            hour_names.append(f"{h-12}:00 PM")
    
    pivoted.columns = hour_names
    
    # Ensure all 24 columns exist, even if no data for some hours
    expected_cols = hour_names
    for col in expected_cols:
        if col not in pivoted.columns:
            pivoted[col] = np.nan
            
    pivoted = pivoted[expected_cols]
    
    # Format date column
    pivoted.index = pivoted.index.strftime('%m/%d/%Y')
    pivoted = pivoted.reset_index()
    pivoted = pivoted.rename(columns={'date_only': 'date'})
    
    return pivoted
