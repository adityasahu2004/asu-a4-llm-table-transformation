import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    # Format is M/D/YYYY H:MM
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date string for grouping and hour for pivoting
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hour to 12-hour format labels
    def get_hour_label(h):
        if h == 0:
            return "12:00 AM"
        elif h < 12:
            return f"{h}:00 AM"
        elif h == 12:
            return "12:00 PM"
        else:
            return f"{h-12}:00 PM"
            
    df['hour_label'] = df['hour'].apply(get_hour_label)
    
    # 4. Pivot the data
    # We use 'first' aggregation in case there are multiple entries for the same hour/day,
    # though the sample suggests sparse or unique entries.
    pivoted = df.pivot_table(
        index='date_str', 
        columns='hour_label', 
        values='zone_016', 
        aggfunc='first'
    )
    
    # 5. Define the expected column order
    hour_labels = []
    # 1 AM to 11 AM
    for h in range(1, 12):
        hour_labels.append(f"{h}:00 AM")
    # 12 PM
    hour_labels.append("12:00 PM")
    # 1 PM to 11 PM
    for h in range(1, 12):
        hour_labels.append(f"{h}:00 PM")
    # 12 AM
    hour_labels.append("12:00 AM")
    
    # 6. Reindex columns to ensure all 24 hours are present and in order
    pivoted = pivoted.reindex(columns=hour_labels)
    
    # 7. Reset index to make date a column
    result = pivoted.reset_index()
    
    # 8. Rename index column to 'date'
    result = result.rename(columns={'date_str': 'date'})
    
    # 9. Sort by date descending as per target sample (01/02/2018 before 01/01/2018)
    # The target sample shows 01/02/2018 first, then 01/01/2018.
    result = result.sort_values(by='date', ascending=False).reset_index(drop=True)
    
    return result
