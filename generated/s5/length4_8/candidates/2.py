import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date and hour
    df['date_key'] = df['dt'].dt.date
    df['hour'] = df['dt'].dt.hour
    
    # Map hour to target column name
    def hour_to_label(h):
        if h == 0:
            return "12:00 AM"
        elif 1 <= h <= 11:
            return f"{h}:00 AM"
        elif h == 12:
            return "12:00 PM"
        else:
            return f"{h-12}:00 PM"
            
    df['hour_label'] = df['hour'].apply(hour_to_label)
    
    # Pivot: Group by date and hour_label, aggregate (mean handles duplicates if any, otherwise just the value)
    pivot_df = df.groupby(['date_key', 'hour_label'])['cerc_logger_1'].mean().reset_index()
    
    # Pivot table
    result = pivot_df.pivot(index='date_key', columns='hour_label', values='cerc_logger_1')
    
    # Define the desired column order
    hour_order = [
        "1:00 AM", "2:00 AM", "3:00 AM", "4:00 AM", "5:00 AM", "6:00 AM", 
        "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
        "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM", 
        "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM", "12:00 AM"
    ]
    
    # Ensure all columns are present, even if NaN for some dates
    for col in hour_order:
        if col not in result.columns:
            result[col] = np.nan
            
    # Select and order columns
    result = result[hour_order]
    
    # Reset index to make date a column
    result = result.reset_index()
    
    # Format date column as MM/DD/YYYY
    result['date'] = pd.to_datetime(result['date_key']).dt.strftime('%m/%d/%Y')
    
    # Drop the helper date_key column
    result = result.drop(columns=['date_key'])
    
    # Rename 'date' to match target exactly (it is already 'date')
    
    return result
