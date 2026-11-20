import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Define function to convert hour to target time string
    def hour_to_time_str(h):
        if h == 0:
            return "12:00 AM"
        elif h < 12:
            return f"{h}:00 AM"
        elif h == 12:
            return "12:00 PM"
        else:
            return f"{h-12}:00 PM"
            
    df['time_label'] = df['hour'].apply(hour_to_time_str)
    
    # 4. Pivot the data
    # We group by date_only and time_label to handle potential duplicates (though unlikely in clean hourly data)
    # Using pivot_table with mean to aggregate if duplicates exist, or just pivot if unique
    pivot_df = df.pivot_table(
        index='date_only', 
        columns='time_label', 
        values='zone_016_cooling_sp', 
        aggfunc='first' # Take first value if duplicates exist
    )
    
    # 5. Define the specific column order required by the target
    # Order: 1 AM, 2 AM, ..., 11 AM, 12 PM, 1 PM, ..., 11 PM, 12 AM
    time_cols_ordered = []
    for h in range(1, 12): # 1 AM to 11 AM
        time_cols_ordered.append(f"{h}:00 AM")
    time_cols_ordered.append("12:00 PM") # 12 PM
    for h in range(1, 12): # 1 PM to 11 PM
        time_cols_ordered.append(f"{h}:00 PM")
    time_cols_ordered.append("12:00 AM") # 12 AM (Hour 0)
    
    # Ensure all expected columns exist, filling with NaN if missing
    for col in time_cols_ordered:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # Select and reorder columns
    pivot_df = pivot_df[time_cols_ordered]
    
    # 6. Format the date index back to string MM/DD/YYYY
    pivot_df.index = pd.to_datetime(pivot_df.index).strftime('%m/%d/%Y')
    
    # 7. Reset index to make 'date' a column
    result = pivot_df.reset_index()
    result = result.rename(columns={'index': 'date'})
    
    return result
