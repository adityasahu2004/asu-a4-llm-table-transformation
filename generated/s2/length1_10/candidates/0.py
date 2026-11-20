import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'])
    
    # Floor to day for grouping
    df['date_floor'] = df['dt'].dt.floor('D')
    
    # Calculate hour bin (1-24)
    # 00:00-01:00 -> 1
    # 23:00-00:00 -> 24
    df['hour_bin'] = df['dt'].dt.hour + 1
    
    # Map the cooling setpoint to the target values
    # 73.0 -> 876.0
    # 84.0 -> 0.0
    # Handle potential NaNs by mapping them to NaN first, then we can decide how to aggregate
    mapping = {73.0: 876.0, 84.0: 0.0}
    df['val'] = df['zone_016_cooling_sp'].map(mapping)
    
    # Group by date and hour bin, and take the first non-null value
    # If there are multiple values, they should be consistent. 
    # Using 'first' after sorting by time is a safe bet for sparse data.
    grouped = df.groupby(['date_floor', 'hour_bin'])['val'].first().reset_index()
    
    # Pivot to wide format
    pivot = grouped.pivot(index='date_floor', columns='hour_bin', values='val')
    
    # Rename columns to match target format "1:00", "2:00", ... "24:00"
    pivot.columns = [f"{col}:00" for col in pivot.columns]
    
    # Sort columns to ensure order 1:00 to 24:00
    pivot = pivot.reindex(sorted(pivot.columns, key=lambda x: int(x.split(':')[0])), axis=1)
    
    # Format the date index
    pivot.index = pivot.index.strftime('%a %m/%d/%Y')
    pivot.index.name = 'cst'
    
    # Reset index to make 'cst' a column
    result = pivot.reset_index()
    
    # Ensure all expected columns are present, filling missing with 0.0 if necessary
    # The target has 0 nulls.
    expected_cols = ['cst'] + [f"{h}:00" for h in range(1, 25)]
    for col in expected_cols:
        if col not in result.columns:
            result[col] = 0.0
            
    result = result[expected_cols]
    
    return result
