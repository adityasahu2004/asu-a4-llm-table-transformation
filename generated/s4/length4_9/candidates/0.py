import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'])
    
    # Extract date and hour
    df['cal_date'] = df['dt'].dt.date
    df['hour'] = df['dt'].dt.hour
    
    # Map hour to 12-hour AM/PM label
    def get_label(h):
        if h == 0:
            return "12:00 AM"
        elif h == 12:
            return "12:00 PM"
        elif h < 12:
            return f"{h}:00 AM"
        else:
            return f"{h-12}:00 PM"
            
    df['hour_label'] = df['hour'].apply(get_label)
    
    # Pivot
    pivoted = df.pivot_table(index='cal_date', columns='hour_label', values='zone_016', aggfunc='first')
    
    # Format date index
    pivoted.index = pivoted.index.strftime('%m/%d/%Y')
    pivoted = pivoted.reset_index()
    pivoted.rename(columns={'index': 'date'}, inplace=True)
    
    # Define target column order
    target_cols = ['date']
    # 1:00 AM to 11:00 AM
    for h in range(1, 12):
        target_cols.append(f"{h}:00 AM")
    # 12:00 PM
    target_cols.append("12:00 PM")
    # 1:00 PM to 11:00 PM
    for h in range(1, 12):
        target_cols.append(f"{h}:00 PM")
    # 12:00 AM
    target_cols.append("12:00 AM")
    
    # Select and reorder columns, ensuring all exist (fillna if necessary, though pivot should handle structure)
    # The target shows specific order. We must ensure columns present.
    result = pivoted[target_cols]
    
    return result

transform
