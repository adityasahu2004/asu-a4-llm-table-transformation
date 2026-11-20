import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    df['date_key'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Map hour to 12-hour format string
    def format_hour(h):
        if h == 0:
            return "12:00 AM"
        elif h < 12:
            return f"{h}:00 AM"
        elif h == 12:
            return "12:00 PM"
        else:
            return f"{h-12}:00 PM"
    
    df['hour_label'] = df['hour'].apply(format_hour)
    
    # Pivot
    pivoted = df.pivot_table(index='date_key', columns='hour_label', values='cerc_logger_1', aggfunc='first')
    
    # Ensure all 24 columns exist and are in order
    hour_labels = []
    for h in range(24):
        hour_labels.append(format_hour(h))
        
    # Reindex columns to ensure order and presence
    pivoted = pivoted.reindex(columns=hour_labels)
    
    # Rename index to 'date' and format it
    pivoted.index.name = 'date'
    pivoted['date'] = pivoted.index.strftime('%m/%d/%Y')
    
    # Move date column to front
    cols = ['date'] + hour_labels
    result = pivoted[cols]
    
    return result.reset_index(drop=True)
