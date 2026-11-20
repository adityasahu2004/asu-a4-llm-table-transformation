import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date string for grouping
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # Extract hour (0-23) and map to "Hour 1" - "Hour 24"
    df['hour_label'] = df['datetime'].dt.hour.apply(lambda h: f'Hour {h + 1}')
    
    # Aggregate: Since each timestamp is unique, we might just have one value per hour per day.
    # If there are multiple, mean is a safe default for sensor data.
    pivot_table = df.groupby(['date_str', 'hour_label'])['cerc_logger_1'].mean()
    
    # Unstack to get hours as columns
    result = pivot_table.unstack(level='hour_label')
    
    # Rename columns to ensure they are strings and in correct format
    result.columns = [f'Hour {i}' for i in range(1, 25)]
    
    # Reset index to make date_str a column
    result = result.reset_index()
    
    # Rename date_str to date
    result = result.rename(columns={'date_str': 'date'})
    
    # Ensure column order matches target: date, Hour 1, ..., Hour 24
    cols = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    result = result[cols]
    
    # Sort by date? The target sample isn't strictly sorted chronologically in the snippet provided 
    # (05/08/2019, 07/13/2019, 07/09/2018...), but usually datasets are sorted. 
    # The prompt says "Infer a general transformation". The target sample order is arbitrary.
    # We will leave it in the order produced by groupby (sorted by date_str).
    
    return result
