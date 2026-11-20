import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format in source: "m/d/Y H:MM" e.g., "1/2/2018 0:11"
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'])
    
    # Extract date for grouping and formatting
    df['date_only'] = df['dt'].dt.date
    df['dt_strata'] = df['dt'].dt.strftime('%m/%d/%y')
    df['dow'] = df['dt'].dt.dayofweek + 1  # Monday=1 ... Sunday=7
    
    # Extract hour (0-23)
    df['hour'] = df['dt'].dt.hour
    
    # Map hour to target column index (1-24)
    # Source Hour 0 -> Target Col 1 (pct_hourly_0100)
    # Source Hour 23 -> Target Col 24 (pct_hourly_2400)
    df['target_col_idx'] = df['hour'] + 1
    
    # Create the target column names
    target_cols = [f'pct_hourly_{i:02d}00' for i in range(1, 25)]
    
    # Pivot the data
    # We need to aggregate zone_016 by date_only and target_col_idx
    # Since the target has one row per date, we group by date_only
    # We'll use pivot_table or groupby + unstack
    
    # Filter out nulls in zone_016 if necessary, or let them become NaN then fill 0
    # The target has 0.0 for missing hours.
    
    # Create a long format with explicit column names
    df['target_col_name'] = df['target_col_idx'].apply(lambda x: f'pct_hourly_{x:02d}00')
    
    # Pivot
    pivot_df = df.pivot_table(
        index=['date_only', 'dt_strata', 'dow'],
        columns='target_col_name',
        values='zone_016',
        aggfunc='first' # Or mean/sum, 'first' is safe if unique per hour
    )
    
    # Reset index
    pivot_df = pivot_df.reset_index()
    
    # Ensure all 24 columns exist and are in order, fill NaN with 0
    for col in target_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0.0
        else:
            pivot_df[col] = pivot_df[col].fillna(0.0)
            
    # Select and order columns
    result_cols = ['dt_strata', 'dow'] + target_cols
    pivot_df = pivot_df[result_cols]
    
    # Add pct_hourly_2500 = 0
    pivot_df['pct_hourly_2500'] = 0
    
    # Drop date_only helper
    pivot_df = pivot_df.drop(columns=['date_only'])
    
    # Sort? The sample shows Jan 2 then Jan 1. 
    # Usually, we preserve input order or sort by date. 
    # The target sample is not sorted chronologically. 
    # We will sort by dt_strata descending to match the sample appearance? 
    # Or just return as is. The prompt doesn't specify order. 
    # However, to be safe, let's sort by dt_strata descending as seen in sample (01/02 before 01/01).
    pivot_df = pivot_df.sort_values('dt_strata', ascending=False).reset_index(drop=True)
    
    # Ensure dtypes
    pivot_df['dow'] = pivot_df['dow'].astype(int)
    pivot_df['pct_hourly_2500'] = pivot_df['pct_hourly_2500'].astype(int)
    for col in target_cols:
        pivot_df[col] = pivot_df[col].astype(float)
        
    return pivot_df
