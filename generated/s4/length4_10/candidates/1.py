import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date and hour
    df['date_key'] = df['dt'].dt.date
    df['hour'] = df['dt'].dt.hour
    
    # Pivot: index=date_key, columns=hour, values=zone_016_cooling_sp
    # This aggregates implicitly if there are multiple entries per hour/day (mean/sum/etc).
    # Given the distinct values and structure, it seems to be one value per hour or consistent.
    # Using 'first' or 'mean' is safe if unique, but pivot_table handles duplicates.
    # Let's use pivot_table with mean to be safe against duplicates, though data suggests unique.
    pivoted = df.pivot_table(index='date_key', columns='hour', values='zone_016_cooling_sp', aggfunc='mean')
    
    # Reset index to make date_key a column
    pivoted = pivoted.reset_index()
    
    # Rename hour columns to AM/PM format
    def format_hour(h):
        if h == 0:
            return "12:00 AM"
        elif h < 12:
            return f"{h}:00 AM"
        elif h == 12:
            return "12:00 PM"
        else:
            return f"{h-12}:00 PM"
            
    new_cols = {}
    for h in range(24):
        if h in pivoted.columns:
            new_cols[h] = format_hour(h)
            
    pivoted.rename(columns=new_cols, inplace=True)
    
    # Format date column
    pivoted['date'] = pivoted['date_key'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # Drop the original date_key column
    pivoted.drop(columns=['date_key'], inplace=True)
    
    # Reorder columns: date first, then hours 0-23 (which are now 12AM, 1AM... 11PM)
    # The target order is 1:00 AM, 2:00 AM ... 12:00 AM.
    # Wait, let's look at target column order:
    # "1:00 AM", "2:00 AM", ..., "11:00 AM", "12:00 PM", "1:00 PM", ..., "11:00 PM", "12:00 AM"
    # This corresponds to hours 1, 2, ..., 11, 12, 13, ..., 23, 0.
    
    ordered_hour_cols = [format_hour(h) for h in range(1, 24)] + [format_hour(0)]
    
    # Ensure all columns exist
    final_cols = ['date'] + ordered_hour_cols
    
    # Select and reorder
    result = pivoted[final_cols]
    
    return result
