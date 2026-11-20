import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Define the target column names for the hours
    # Order: 1-11 AM, 12 AM, 1-11 PM, 12 PM
    hour_columns = [
        "1:00 AM", "2:00 AM", "3:00 AM", "4:00 AM", "5:00 AM", "6:00 AM", 
        "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM",
        "12:00 AM",
        "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM", 
        "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM",
        "12:00 PM"
    ]
    
    # Map source value columns to target hour columns
    # value1 -> 1:00 AM, value2 -> 2:00 AM, ..., value24 -> 12:00 PM
    rename_map = {f"value{i+1}": col for i, col in enumerate(hour_columns)}
    
    # Select the date and value columns
    df = source[['date'] + [f"value{i+1}" for i in range(24)]].copy()
    
    # Rename the value columns to the target hour names
    df.rename(columns=rename_map, inplace=True)
    
    # Parse the date and format it to 'YYYY-MM-DD 00:00:00'
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d 00:00:00')
    
    # Reorder columns to match target specification exactly
    # Target order: date, then the hour columns in the specific order defined above
    final_columns = ['date'] + hour_columns
    df = df[final_columns]
    
    return df
