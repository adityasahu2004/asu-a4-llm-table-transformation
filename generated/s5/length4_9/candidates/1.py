import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Create grouping date string MM/DD/YYYY
    df['date_str'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # Extract hour
    df['hour'] = df['dt'].dt.hour
    
    # Map hour to 12-hour clock string
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
    pivot_table = df.pivot_table(
        index='date_str',
        columns='hour_label',
        values='zone_016',
        aggfunc='first' # Assuming unique per date/hour, first is safe
    )
    
    # Reset index to make date a column
    pivot_table = pivot_table.reset_index()
    
    # Define the desired column order
    # 1 AM, 2 AM, ..., 11 AM, 12 PM, 1 PM, ..., 11 PM, 12 AM
    cols_ordered = []
    # AM hours 1-11
    for h in range(1, 12):
        cols_ordered.append(f"{h}:00 AM")
    # 12 PM
    cols_ordered.append("12:00 PM")
    # PM hours 1-11
    for h in range(1, 12):
        cols_ordered.append(f"{h}:00 PM")
    # 12 AM
    cols_ordered.append("12:00 AM")
    
    # Ensure all columns exist in pivot_table (fill with NaN if missing)
    for col in cols_ordered:
        if col not in pivot_table.columns:
            pivot_table[col] = np.nan
            
    # Select and reorder columns
    result = pivot_table[['date'] + cols_ordered]
    result = result.rename(columns={'date': 'date'})
    
    # Sort by date descending to match sample
    result = result.sort_values('date', ascending=False).reset_index(drop=True)
    
    return result
