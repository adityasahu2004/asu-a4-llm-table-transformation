import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract Hour and Month
    df['Hour'] = df['datetime'].dt.hour
    df['Month'] = df['datetime'].dt.month
    
    # Pivot the data
    # Index: Hour, Columns: Month, Values: zone_016_cooling_sp
    pivot_df = df.pivot_table(index='Hour', columns='Month', values='zone_016_cooling_sp', aggfunc='first')
    
    # Rename month columns to full names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    pivot_df.rename(columns=month_names, inplace=True)
    
    # Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # Ensure Hour is integer
    pivot_df['Hour'] = pivot_df['Hour'].astype(int)
    
    # Sort by Hour to ensure 0-23 order
    pivot_df = pivot_df.sort_values('Hour').reset_index(drop=True)
    
    # Define the expected column order
    expected_cols = ['Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
                     'July', 'August', 'September', 'October', 'November', 'December']
    
    # Reindex to ensure all month columns are present, even if empty
    pivot_df = pivot_df.reindex(columns=expected_cols)
    
    return pivot_df
