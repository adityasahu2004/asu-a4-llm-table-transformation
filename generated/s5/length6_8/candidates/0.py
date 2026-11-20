import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date for grouping and hour for pivoting
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Pivot the data
    # We want 'date_only' as index, 'hour' as columns, and 'cerc_logger_1' as values
    # Using pivot_table to handle potential duplicates with mean aggregation
    pivot_df = df.pivot_table(index='date_only', columns='hour', values='cerc_logger_1', aggfunc='mean')
    
    # Reindex columns to ensure all hours 0-23 are present
    pivot_df = pivot_df.reindex(columns=range(24), fill_value=np.nan)
    
    # Rename columns to match target: Hr 1, Hr 2, ..., Hr 24
    # Hour 0 becomes Hr 1, Hour 1 becomes Hr 2, etc.
    pivot_df.columns = [f'Hr {h+1}' for h in pivot_df.columns]
    
    # Create the Date column formatted as MM/DD/YYYY
    pivot_df['Date'] = pivot_df.index.strftime('%m/%d/%Y')
    
    # Reset index and select columns in the correct order
    result = pivot_df.reset_index(drop=True)
    result = result[['Date'] + [f'Hr {h}' for h in range(1, 25)]]
    
    return result
