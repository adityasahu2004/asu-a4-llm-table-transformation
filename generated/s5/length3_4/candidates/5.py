import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date string and hour
    df['date_str'] = df['dt'].dt.strftime('%m/%d/%Y')
    df['hour'] = df['dt'].dt.hour
    
    # Map hour to target column names: 0 -> Hour 24, 1-23 -> Hour 1-23
    def map_hour(h):
        if h == 0:
            return 'Hour 24'
        else:
            return f'Hour {h}'
            
    df['col_name'] = df['hour'].apply(map_hour)
    
    # Pivot the data
    # Using 'first' as aggregation function since values are consistent per hour in the sample
    pivot_df = df.pivot_table(
        index='date_str', 
        columns='col_name', 
        values='zone_016_cooling_sp', 
        aggfunc='first'
    ).reset_index()
    
    # Rename index column to 'date'
    pivot_df = pivot_df.rename(columns={'date_str': 'date'})
    
    # Ensure all hour columns exist and are in the correct order
    expected_cols = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # Reindex columns to ensure order and presence
    pivot_df = pivot_df.reindex(columns=expected_cols)
    
    # Cast Hour 10 to Hour 21 to int64 as per target schema
    # The target schema indicates these columns have 0 nulls, so direct cast is safe
    int_cols = [f'Hour {i}' for i in range(10, 22)]
    for col in int_cols:
        if col in pivot_df.columns:
            # Fill NaNs with 0 if any exist unexpectedly, though schema says 0 nulls
            # But to be safe and deterministic, we only cast if no nulls or handle them
            # Given the constraint "Preserve NaNs unless...", and target says 0 nulls for these,
            # we assume they are present.
            pivot_df[col] = pivot_df[col].astype('int64')
            
    return pivot_df
