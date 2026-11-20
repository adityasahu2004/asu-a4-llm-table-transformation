import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date string for the index
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # Extract hour
    df['hour'] = df['datetime'].dt.hour
    
    # Map hour to target label
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
    
    # Pivot the table
    # Index: date_str, Columns: hour_label, Values: zone_016_cooling_sp
    pivoted = df.pivot_table(index='date_str', columns='hour_label', values='zone_016_cooling_sp', aggfunc='first')
    
    # Define the specific column order required by the target
    # 1:00 AM to 11:00 AM
    cols_am = [f"{h}:00 AM" for h in range(1, 12)]
    # 12:00 PM
    cols_pm = ["12:00 PM"]
    # 1:00 PM to 11:00 PM
    cols_pm_rest = [f"{h}:00 PM" for h in range(1, 12)]
    # 12:00 AM (Hour 0)
    cols_midnight = ["12:00 AM"]
    
    final_cols = cols_am + cols_pm + cols_pm_rest + cols_midnight
    
    # Reorder columns, filling NaNs if a specific hour is missing for a day (though pivot usually handles this)
    # The target shows nulls for some hours, so we just select the columns.
    # If a column is missing from the pivot (e.g. no data for 12:00 AM on a specific day), it will be NaN.
    
    result = pivoted.reindex(columns=final_cols)
    
    # Reset index to make 'date' a column
    result = result.reset_index()
    result.rename(columns={'date_str': 'date'}, inplace=True)
    
    return result
