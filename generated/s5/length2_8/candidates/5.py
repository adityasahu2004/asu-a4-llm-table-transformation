import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format: m/d/yyyy H:MM
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract components
    df['dt_strata'] = df['datetime'].dt.strftime('%m/%d/%y')
    df['dow'] = df['datetime'].dt.dayofweek # 0=Mon, 6=Sun
    df['hour'] = df['datetime'].dt.hour
    
    # Map hour to target column name
    # Hour 0 -> pct_hourly_0100
    # Hour 1 -> pct_hourly_0200
    # ...
    # Hour 23 -> pct_hourly_2400
    df['hour_col'] = df['hour'].apply(lambda h: f'pct_hourly_{h+1:02d}00')
    
    # Aggregate by date and hour
    # We take the mean of the values for each hour in each day
    # If there are multiple readings per hour, average them.
    agg_df = df.groupby(['dt_strata', 'dow', 'hour_col'])['cerc_logger_1'].mean().reset_index()
    
    # Pivot to wide format
    pivot_df = agg_df.pivot_table(index=['dt_strata', 'dow'], columns='hour_col', values='cerc_logger_1', fill_value=0.0)
    
    # Reset index to make dt_strata and dow columns
    pivot_df = pivot_df.reset_index()
    
    # Ensure all 24 columns exist and are in order
    expected_cols = [f'pct_hourly_{h:02d}00' for h in range(1, 25)]
    
    # Reindex columns to ensure order and presence
    for col in expected_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0.0
            
    # Select and order columns
    result_cols = ['dt_strata', 'dow'] + expected_cols
    pivot_df = pivot_df[result_cols]
    
    # Add the 25th hour column with 0
    pivot_df['pct_hourly_2500'] = 0
    
    # Sort by dt_strata to match typical output expectations, 
    # though the sample order is ambiguous. 
    # The sample shows 01/14, 02/19, 02/26, 01/07... 
    # This is not sorted by date. It might be sorted by the original appearance or dow.
    # However, without explicit instruction, sorting by date is the most deterministic.
    # Let's check if the sample is sorted by dow? 
    # 01/14 (Mon, 1), 02/19 (Tue, 2), 02/26 (Tue, 2), 01/07 (Mon, 1). 
    # It's not strictly sorted by dow either.
    # I will sort by dt_strata.
    pivot_df = pivot_df.sort_values('dt_strata').reset_index(drop=True)
    
    return pivot_df
