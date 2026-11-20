import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract calendar date for grouping
    df['cal_date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # Determine target hour label
    def get_hour_label(dt):
        h = dt.hour
        if h == 0:
            return '12:00 AM'
        elif h < 12:
            return f'{h}:00 AM'
        elif h == 12:
            return '12:00 PM'
        else:
            return f'{h-12}:00 PM'
            
    df['hour_label'] = df['datetime'].apply(get_hour_label)
    
    # Pivot
    pivot_df = df.pivot_table(index='cal_date', columns='hour_label', values='zone_016', aggfunc='first')
    
    # Define the desired column order
    hour_order = []
    for h in range(1, 13):
        hour_order.append(f'{h}:00 AM')
    hour_order.append('12:00 PM')
    for h in range(1, 12):
        hour_order.append(f'{h}:00 PM')
    hour_order.append('12:00 AM')
    
    # Reindex columns to match desired order, adding NaN for missing columns if any
    pivot_df = pivot_df.reindex(columns=hour_order)
    
    # Rename index to date
    pivot_df.index.name = 'date'
    pivot_df = pivot_df.reset_index()
    
    return pivot_df
