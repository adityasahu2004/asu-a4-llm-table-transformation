import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    # Source format: "7/28/2019 4:50" -> M/D/YYYY H:MM
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %I:%M %p', errors='coerce')
    
    # If the above format fails due to single digit hours/minutes without leading zeros or AM/PM,
    # try a more flexible parser or specific format.
    # The sample "7/28/2019 4:50" suggests 12-hour clock? Or 24-hour?
    # "4:50" could be 4:50 AM or 4:50 PM. 
    # Let's check "12:20" in sample. If it's 24h, 12:20 is noon. If 12h, it's noon.
    # "18:50" in sample clearly indicates 24-hour format.
    # So the format is likely %m/%d/%Y %H:%M
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M', errors='coerce')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour_idx'] = df['datetime'].dt.hour # 0-23
    
    # 3. Pivot the data
    # We want columns "Hour 1" to "Hour 24"
    # Mapping: hour_idx 0 -> "Hour 1", hour_idx 1 -> "Hour 2", ..., hour_idx 23 -> "Hour 24"
    
    # Create a mapping for column names
    hour_map = {i: f"Hour {i+1}" for i in range(24)}
    df['hour_label'] = df['hour_idx'].map(hour_map)
    
    # Pivot table
    # Index: date_only
    # Columns: hour_label
    # Values: cerc_logger_1
    # Aggfunc: mean (to handle potential duplicates, though likely unique)
    pivoted = df.pivot_table(
        index='date_only',
        columns='hour_label',
        values='cerc_logger_1',
        aggfunc='mean'
    )
    
    # 4. Reset index and rename date column
    pivoted = pivoted.reset_index()
    pivoted = pivoted.rename(columns={'date_only': 'date'})
    
    # 5. Ensure all 24 hour columns exist, even if empty
    expected_hours = [f"Hour {i+1}" for i in range(24)]
    for h in expected_hours:
        if h not in pivoted.columns:
            pivoted[h] = np.nan
            
    # 6. Select and order columns
    # Target order: date, Hour 1, ..., Hour 24
    final_columns = ['date'] + expected_hours
    result = pivoted[final_columns]
    
    # 7. Format date column to MM/DD/YYYY
    # Convert date object to datetime then to string
    result['date'] = pd.to_datetime(result['date']).dt.strftime('%m/%d/%Y')
    
    # 8. Sort by date to ensure consistent ordering (optional but good practice)
    # The target sample isn't strictly sorted, but usually these outputs are.
    # However, the prompt says "Preserve NaNs...". Sorting doesn't affect NaNs.
    # Let's sort by date string to match typical expectations.
    result = result.sort_values('date').reset_index(drop=True)
    
    return result
