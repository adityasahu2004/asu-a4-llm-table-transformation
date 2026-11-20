import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date string to datetime
    # Format in source: "m/d/Y H:M" (e.g., "7/28/2019 4:50")
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %I:%M%p', errors='coerce')
    
    # If format above fails, try flexible parsing or specific pattern
    # The sample has "7/28/2019 4:50". No AM/PM.
    # So it's 24-hour or 12-hour without indicator? 
    # "4:50" is ambiguous. But "18:50" is in sample. So it's 24-hour.
    # Format: %m/%d/%Y %H:%M
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date for grouping and hour for pivot
    df['dt'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Map hour 0-23 to target column names 1:00 - 24:00
    # Hour 0 -> 1:00
    # Hour 23 -> 24:00
    df['hour_col'] = df['hour'].apply(lambda h: f'{h + 1}:00')
    
    # Group by date and hour column, sum the values
    # Use sort=False to preserve the order of first appearance in the source
    grouped = df.groupby(['dt', 'hour_col'], sort=False)['cerc_logger_1'].sum()
    
    # Pivot to wide format
    result = grouped.unstack(fill_value=0)
    
    # Ensure all 24 columns are present and in order
    expected_cols = [f'{h}:00' for h in range(1, 25)]
    # Reindex to ensure all columns exist, filling missing with 0
    result = result.reindex(columns=expected_cols, fill_value=0)
    
    # Convert index (dt) to string format for 'cst'
    # Format: "Sat 07/20/2019" -> %a %m/%d/%Y
    result['cst'] = pd.to_datetime(result.index).dt.strftime('%a %m/%d/%Y')
    
    # Move 'cst' to the front
    cols = ['cst'] + expected_cols
    result = result[cols]
    
    # Reset index to make 'dt' a column if needed, but we converted it to 'cst'
    # The index is currently the datetime object.
    result = result.reset_index(drop=True)
    
    return result
