import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format in sample: "7/28/2019 4:50" -> "%m/%d/%Y %H:%M"
    # Note: Single digit months/days/hours are possible.
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date part and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Map hour 0->1, 1->2, ..., 23->24
    df['hour_label'] = df['hour'] + 1
    
    # Create column names
    hour_cols = [f"Hour {i}" for i in range(1, 25)]
    
    # Pivot the data
    # index: date_only, columns: hour_label, values: cerc_logger_1
    # Using pivot_table with mean to handle potential duplicates, though likely 1:1
    pivoted = df.pivot_table(
        index='date_only', 
        columns='hour_label', 
        values='cerc_logger_1', 
        aggfunc='mean'
    )
    
    # Ensure all hour columns are present and in order
    pivoted = pivoted.reindex(columns=hour_cols)
    
    # Reset index to make date a column
    pivoted = pivoted.reset_index()
    
    # Format date as MM/DD/YYYY
    pivoted['date'] = pivoted['date_only'].dt.strftime('%m/%d/%Y')
    
    # Drop the helper column 'date_only' if it was kept as index name
    if 'date_only' in pivoted.columns:
        pivoted = pivoted.drop(columns=['date_only'])
        
    # Rename the index column from 'date_only' (if it became index name) to 'date' is handled by reset_index + rename above
    # The column 'date' is now the formatted string.
    
    # Select and order columns
    final_cols = ['date'] + hour_cols
    result = pivoted[final_cols]
    
    return result
