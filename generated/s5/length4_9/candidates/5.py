import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    # Format is M/d/yyyy H:mm (e.g., "1/2/2018 0:11")
    source = source.copy()
    source['parsed_dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    source['cal_date'] = source['parsed_dt'].dt.date
    source['hour'] = source['parsed_dt'].dt.hour
    
    # 3. Map hour to target column labels
    # 0 -> 12:00 AM, 1 -> 1:00 AM, ..., 11 -> 11:00 AM
    # 12 -> 12:00 PM, 13 -> 1:00 PM, ..., 23 -> 11:00 PM
    def map_hour_label(h):
        if h == 0:
            return "12:00 AM"
        elif h < 12:
            return f"{h}:00 AM"
        elif h == 12:
            return "12:00 PM"
        else:
            return f"{h-12}:00 PM"
            
    source['hour_label'] = source['hour'].apply(map_hour_label)
    
    # 4. Pivot the data
    # Index: cal_date, Columns: hour_label, Values: zone_016
    pivoted = source.pivot_table(
        index='cal_date', 
        columns='hour_label', 
        values='zone_016', 
        aggfunc='first' # Assuming unique per hour per day, or just take first
    )
    
    # 5. Format the date index to MM/dd/yyyy
    pivoted.index = pivoted.index.strftime('%m/%d/%Y')
    pivoted.index.name = 'date'
    
    # 6. Reorder columns to match target schema order
    # Target order: 1:00 AM ... 11:00 PM, 12:00 AM
    ordered_labels = []
    for h in range(1, 13):
        ordered_labels.append(f"{h}:00 AM")
    for h in range(12, 24):
        if h == 12:
            ordered_labels.append("12:00 PM")
        else:
            ordered_labels.append(f"{h-12}:00 PM")
    ordered_labels.append("12:00 AM")
    
    # Filter to only existing columns in the correct order
    existing_cols = [col for col in ordered_labels if col in pivoted.columns]
    pivoted = pivoted[existing_cols]
    
    # 7. Reset index to make 'date' a column
    result = pivoted.reset_index()
    
    return result
