import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date string to datetime
    # Format in source: "M/D/YYYY H:MM"
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M', errors='coerce')
    
    # Extract date and hour
    # Note: pd.to_datetime might infer format, but explicit is safer. 
    # However, the sample shows "1/2/2018 0:11".
    # Let's try parsing without explicit format first if possible, or use mixed.
    # Actually, the sample data has variable width for month/day.
    # pd.to_datetime handles "1/2/2018 0:11" correctly by default usually.
    # But let's be safe.
    try:
        df['datetime'] = pd.to_datetime(df['date'])
    except:
        df['datetime'] = pd.to_datetime(df['date'], format='mixed')

    df['date_key'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Map hour 0-23 to Hr 1-24
    # Hr 1 corresponds to hour 0
    # Hr 24 corresponds to hour 23
    df['hr_label'] = df['hour'].apply(lambda h: f'Hr {h + 1}')
    
    # Pivot the table
    # Index: date_key
    # Columns: hr_label
    # Values: zone_016
    pivoted = df.pivot_table(index='date_key', columns='hr_label', values='zone_016')
    
    # Reset index to make date_key a column
    pivoted = pivoted.reset_index()
    
    # Rename date_key to Date
    pivoted = pivoted.rename(columns={'date_key': 'Date'})
    
    # Format Date as MM/DD/YYYY
    pivoted['Date'] = pivoted['Date'].dt.strftime('%m/%d/%Y')
    
    # Ensure all 24 hour columns exist
    expected_cols = [f'Hr {i}' for i in range(1, 25)]
    for col in expected_cols:
        if col not in pivoted.columns:
            pivoted[col] = np.nan
            
    # Select and order columns
    final_cols = ['Date'] + expected_cols
    result = pivoted[final_cols]
    
    # Sort by Date descending as per sample (01/02/2018 is first)
    # Convert back to datetime for sorting
    result['Date_dt'] = pd.to_datetime(result['Date'])
    result = result.sort_values(by='Date_dt', ascending=False)
    
    # Drop helper column
    result = result.drop(columns=['Date_dt'])
    
    return result.reset_index(drop=True)
