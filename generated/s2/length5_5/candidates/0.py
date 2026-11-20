import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format in source: "m/d/Y H:MM" e.g., "11/6/2018 21:45"
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date part for grouping
    date_part = dt.dt.date
    
    # Extract hour for pivoting
    hour = dt.dt.hour
    
    # Map hour 0 to 24, and 1-23 to 1-23
    # This assumes the data represents 24 hourly slots per day
    hour_idx = hour.replace(0, 24)
    
    # Create a dataframe with date, hour_idx, and value
    df_pivot = pd.DataFrame({
        'date': date_part,
        'hour_idx': hour_idx,
        'value': source['zone_016_cooling_sp']
    })
    
    # Pivot
    # Index: date, Columns: hour_idx, Values: value
    pivoted = df_pivot.pivot(index='date', columns='hour_idx', values='value')
    
    # Ensure columns 1-24 are present
    pivoted = pivoted.reindex(columns=range(1, 25))
    
    # Rename columns to value1...value24
    pivoted.columns = [f'value{i}' for i in range(1, 25)]
    
    # Reset index to make date a column
    pivoted = pivoted.reset_index()
    
    # Format date as MM/DD/YYYY
    pivoted['date'] = pd.to_datetime(pivoted['date']).dt.strftime('%m/%d/%Y')
    
    # Apply type casting
    # value1-value10: float64
    for i in range(1, 11):
        pivoted[f'value{i}'] = pivoted[f'value{i}'].astype('float64')
        
    # value11-value22: int64
    for i in range(11, 23):
        pivoted[f'value{i}'] = pivoted[f'value{i}'].astype('int64')
        
    # value23-value24: float64
    for i in range(23, 25):
        pivoted[f'value{i}'] = pivoted[f'value{i}'].astype('float64')
        
    return pivoted
