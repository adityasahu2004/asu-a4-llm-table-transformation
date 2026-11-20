import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    df['date_only'] = df['dt'].dt.date
    df['hour'] = df['dt'].dt.hour
    
    # Map hour to target column name
    def map_hour(h):
        if h == 0:
            return '12:00 AM'
        elif h == 12:
            return '12:00 PM'
        elif h < 12:
            return f'{h}:00 AM'
        else:
            return f'{h-12}:00 PM'
            
    df['hour_label'] = df['hour'].apply(map_hour)
    
    # Pivot
    pivoted = df.pivot_table(index='date_only', columns='hour_label', values='zone_016_cooling_sp', aggfunc='first')
    
    # Format date index
    pivoted.index = pivoted.index.strftime('%m/%d/%Y')
    pivoted.index.name = 'date'
    
    # Define target column order
    # Target order: 1 AM, 2 AM, ..., 11 AM, 12 PM, 1 PM, ..., 11 PM, 12 AM
    cols_1_to_11_am = [f'{h}:00 AM' for h in range(1, 12)]
    cols_12_pm = ['12:00 PM']
    cols_1_to_11_pm = [f'{h}:00 PM' for h in range(1, 12)]
    cols_12_am = ['12:00 AM']
    
    target_cols = cols_1_to_11_am + cols_12_pm + cols_1_to_11_pm + cols_12_am
    
    # Select and order columns. If a column is missing, it will be NaN, which is correct for nulls.
    result = pivoted[target_cols]
    
    # Reset index to make 'date' a column
    result = result.reset_index()
    
    return result
