import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    # Format is M/D/YYYY H:MM
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hour to target label
    # 0 -> 12:00 AM, 1 -> 1:00 AM, ..., 11 -> 11:00 AM, 12 -> 12:00 PM, 13 -> 1:00 PM, ..., 23 -> 11:00 PM
    def map_hour(h):
        if h == 0:
            return "12:00 AM"
        elif h < 12:
            return f"{h}:00 AM"
        elif h == 12:
            return "12:00 PM"
        else:
            return f"{h-12}:00 PM"
            
    df['hour_label'] = df['hour'].apply(map_hour)
    
    # 4. Pivot the data
    # Group by date_only and hour_label, aggregate the value
    # Using mean to handle potential multiple readings per hour, though likely unique
    pivot_df = df.groupby(['date_only', 'hour_label'])['cerc_logger_1'].mean().unstack(fill_value=np.nan)
    
    # 5. Format the date index
    pivot_df.index = pivot_df.index.strftime('%m/%d/%Y')
    pivot_df.index.name = 'date'
    
    # 6. Define the specific column order
    hour_order = []
    # 1:00 AM to 11:00 AM
    for h in range(1, 12):
        hour_order.append(f"{h}:00 AM")
    # 12:00 PM
    hour_order.append("12:00 PM")
    # 1:00 PM to 11:00 PM
    for h in range(1, 12):
        hour_order.append(f"{h}:00 PM")
    # 12:00 AM
    hour_order.append("12:00 AM")
    
    # Select and reorder columns
    # Ensure all columns exist, though some might be missing if no data for that hour ever
    # The target schema shows all 24 columns.
    result = pivot_df[hour_order]
    
    # Reset index to make 'date' a column
    result = result.reset_index()
    
    return result
