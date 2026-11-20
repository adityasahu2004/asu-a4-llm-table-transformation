import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract the date part and format it as MM/DD/YYYY
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # Extract the hour part and map it to the column index (1-24)
    # Hour 0 -> value1, Hour 1 -> value2, ..., Hour 23 -> value24
    df['hour_col'] = df['datetime'].dt.hour + 1
    
    # Create a pivot table
    # Index: date_str
    # Columns: hour_col
    # Values: zone_016_cooling_sp
    pivot = df.pivot_table(index='date_str', columns='hour_col', values='zone_016_cooling_sp')
    
    # Rename the columns to value1, value2, ..., value24
    pivot.columns = [f'value{h}' for h in pivot.columns]
    
    # Reset the index
    pivot = pivot.reset_index()
    
    # Ensure the date column is a string
    pivot['date'] = pivot['date'].astype(str)
    
    # Reorder the columns
    cols = ['date'] + [f'value{h}' for h in range(1, 25)]
    pivot = pivot[cols]
    
    # Fill NaN values with NaN (already done by pivot_table)
    
    return pivot
