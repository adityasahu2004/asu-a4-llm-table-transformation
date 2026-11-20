import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'])
    
    # Extract date string in MM/DD/YYYY format and hour
    date_str = dt.dt.strftime('%m/%d/%Y')
    hour = dt.dt.hour
    
    # Create a DataFrame for pivoting
    df = pd.DataFrame({
        'date': date_str,
        'hour': hour,
        'value': source['zone_016_cooling_sp']
    })
    
    # Pivot the data. Using pivot to preserve order of appearance if possible, 
    # though order is not strictly defined by the problem, pivot_table sorts.
    # The sample target order is not sorted, so we avoid sorting.
    try:
        pivoted = df.pivot(index='date', columns='hour', values='value')
    except ValueError:
        # If there are duplicate (date, hour) pairs, aggregate them
        pivoted = df.pivot_table(index='date', columns='hour', values='value', aggfunc='first')

    # Rename columns to value1 ... value24
    # Hour 0 -> value1, Hour 23 -> value24
    pivoted.columns = [f'value{i+1}' for i in pivoted.columns]
    
    # Ensure all columns value1...value24 exist
    all_cols = [f'value{i}' for i in range(1, 25)]
    for col in all_cols:
        if col not in pivoted.columns:
            pivoted[col] = np.nan
            
    # Reorder columns
    pivoted = pivoted[all_cols]
    
    # Reset index
    pivoted = pivoted.reset_index()
    
    # Apply specific dtypes
    # value1 - value10: float64
    for i in range(1, 11):
        pivoted[f'value{i}'] = pivoted[f'value{i}'].astype('float64')
        
    # value11 - value22: int64
    # These columns are expected to have no nulls in the target
    for i in range(11, 23):
        pivoted[f'value{i}'] = pivoted[f'value{i}'].astype('int64')
        
    # value23 - value24: float64
    for i in range(23, 25):
        pivoted[f'value{i}'] = pivoted[f'value{i}'].astype('float64')
        
    return pivoted
