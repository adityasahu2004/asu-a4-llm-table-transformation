import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the datetime column
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'])
    
    # Extract date and hour
    df['date_only'] = df['dt'].dt.date
    df['hour'] = df['dt'].dt.hour
    
    # Map hour to 12-hour AM/PM label
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
    
    # Pivot the table
    # Index: date_only, Columns: hour_label, Values: zone_016_cooling_sp
    pivoted = df.pivot_table(
        index='date_only', 
        columns='hour_label', 
        values='zone_016_cooling_sp', 
        aggfunc='first' # Should be unique per date/hour, but 'first' handles potential duplicates safely
    )
    
    # Reset index to make date a column
    pivoted.reset_index(inplace=True)
    
    # Rename date column to 'date' and format as MM/DD/YYYY
    pivoted.rename(columns={'date_only': 'date'}, inplace=True)
    pivoted['date'] = pd.to_datetime(pivoted['date']).dt.strftime('%m/%d/%Y')
    
    # Define the desired column order
    hour_labels = [
        "1:00 AM", "2:00 AM", "3:00 AM", "4:00 AM", "5:00 AM", "6:00 AM", 
        "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
        "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM", 
        "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM", "12:00 AM"
    ]
    
    # Select and order columns
    result_cols = ['date'] + hour_labels
    result = pivoted[result_cols]
    
    # Sort by date for deterministic output
    result.sort_values(by='date', inplace=True)
    
    # Reset index
    result.reset_index(drop=True, inplace=True)
    
    return result
