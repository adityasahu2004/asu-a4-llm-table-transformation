import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the Date column
    # Format: "Thu 10/01/2009" -> "%a %m/%d/%Y"
    source['Date'] = pd.to_datetime(source['Date'], format="%a %m/%d/%Y")
    
    # 2. Create dt_strata: "MM/DD/YY"
    # Example: 2009-10-01 -> "10/01/09"
    # Note: The target sample shows "01/01/03" for a date that is likely 2003-01-01.
    # We format as MM/DD/YY.
    dt_strata = source['Date'].dt.strftime("%m/%d/%y")
    
    # 3. Create dow: 1=Monday, ..., 7=Sunday
    # pandas weekday: 0=Monday, ..., 6=Sunday
    dow = source['Date'].dt.weekday + 1
    
    # 4. Transform hourly columns
    # Source columns: "1:00", "2:00", ..., "23:00", "24:00:00"
    # Target columns: "pct_hourly_0100", ..., "pct_hourly_2400"
    
    # Define mapping from source hour string to target column name
    # We need to handle 1-9 (single digit) and 10-24 (double digit)
    # Source "1:00" -> "01" -> "pct_hourly_0100"
    # Source "10:00" -> "10" -> "pct_hourly_1000"
    # Source "24:00:00" -> "24" -> "pct_hourly_2400"
    
    hourly_cols = [f"{h}:00" if h < 10 else f"{h}:00" for h in range(1, 25)]
    # Adjust for the specific source column names
    # 1-9 are "1:00" to "9:00"
    # 10-23 are "10:00" to "23:00"
    # 24 is "24:00:00"
    
    source_hourly_cols = []
    for h in range(1, 24):
        source_hourly_cols.append(f"{h}:00")
    source_hourly_cols.append("24:00:00")
    
    target_hourly_cols = []
    for h in range(1, 25):
        target_hourly_cols.append(f"pct_hourly_{h:02d}00")
        
    # Create a new dataframe for the hourly data
    # Ensure we select columns that exist in source
    existing_source_cols = [c for c in source_hourly_cols if c in source.columns]
    
    # Map values
    hourly_data = source[existing_source_cols].copy()
    hourly_data.columns = target_hourly_cols[:len(existing_source_cols)]
    
    # If any source columns are missing (unlikely based on schema), fill with NaN
    # But schema says all exist.
    
    # 5. Construct final DataFrame
    result = pd.DataFrame()
    result['dt_strata'] = dt_strata
    result['dow'] = dow
    
    # Add hourly columns
    for col in target_hourly_cols:
        if col in hourly_data.columns:
            result[col] = hourly_data[col]
        else:
            result[col] = np.nan
            
    # Add the all-null column pct_hourly_2500
    result['pct_hourly_2500'] = np.nan
    
    # Ensure column order matches target
    target_columns = ['dt_strata', 'dow'] + target_hourly_cols + ['pct_hourly_2500']
    result = result[target_columns]
    
    return result
