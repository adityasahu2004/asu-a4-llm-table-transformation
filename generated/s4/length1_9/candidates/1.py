import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Map hour 0 to '24:00', others to 'H:00'
    df['hour_label'] = df['hour'].apply(lambda h: '24:00' if h == 0 else f'{h}:00')
    
    # Format the date for the index/column name
    df['date_str'] = df['datetime'].dt.strftime('%a %m/%d/%Y')
    
    # Pivot the table
    # We use date_str as index, hour_label as columns, zone_016 as values
    pivot_df = df.pivot_table(index='date_str', columns='hour_label', values='zone_016', aggfunc='first')
    
    # Fill NaN with 0.0
    pivot_df = pivot_df.fillna(0.0)
    
    # Define the desired column order
    desired_cols = [f'{h}:00' for h in range(1, 25)]
    
    # Reindex columns to match desired order, adding any missing columns as 0.0 if necessary
    # Although pivot_table might only have columns present in data, we want all 24.
    for col in desired_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0.0
            
    pivot_df = pivot_df[desired_cols]
    
    # Reset index to make 'cst' a column
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'date_str': 'cst'})
    
    return pivot_df
