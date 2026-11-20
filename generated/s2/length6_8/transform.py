import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Map hour to target column index
    # Hour 0 -> 24, Hour 1-23 -> 1-23
    df['hr_col'] = df['hour'].apply(lambda h: 24 if h == 0 else h)
    
    # Pivot the data
    pivot_df = df.pivot_table(
        index='date_only',
        columns='hr_col',
        values='cerc_logger_1',
        aggfunc='first' # Assuming one value per hour per day, or take first
    )
    
    # Rename columns to "Hr 1", "Hr 2", ..., "Hr 24"
    pivot_df.columns = [f'Hr {int(col)}' for col in pivot_df.columns]
    
    # Ensure all 24 hours are present, even if null
    all_hours = [f'Hr {h}' for h in range(1, 25)]
    pivot_df = pivot_df.reindex(columns=all_hours)
    
    # Format the date index as MM/DD/YYYY
    pivot_df.index = pivot_df.index.strftime('%m/%d/%Y')
    
    # Reset index to make 'Date' a column
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'index': 'Date'})
    
    return pivot_df
