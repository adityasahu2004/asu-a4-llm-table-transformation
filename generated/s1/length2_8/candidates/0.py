import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'])
    
    # Extract components
    df['dt_strata'] = df['date'].dt.strftime('%m/%d/%y')
    
    # Calculate dow: Mon=1, Tue=2, ..., Sat=6, Sun=0
    # weekday(): Mon=0, ..., Sun=6
    # (weekday + 1) % 7: Mon=1, ..., Sat=6, Sun=0
    df['dow'] = (df['date'].dt.weekday() + 1) % 7
    
    # Determine hour bucket
    # Mapping: Hour 0 -> 24, Hour 1 -> 1, ..., Hour 23 -> 23
    hours = df['date'].dt.hour
    df['hour_bucket'] = hours.replace(0, 24)
    
    # Group by date strata and hour bucket, sum the values
    grouped = df.groupby(['dt_strata', 'hour_bucket'])['cerc_logger_1'].sum().reset_index()
    
    # Pivot to create hourly columns
    pivoted = grouped.pivot(index='dt_strata', columns='hour_bucket', values='cerc_logger_1')
    
    # Fill NaNs with 0.0
    pivoted = pivoted.fillna(0.0)
    
    # Rename columns to match target format pct_hourly_XXXX
    # Ensure all 24 columns exist
    for h in range(1, 25):
        col_name = f'pct_hourly_{h:04d}'
        if h not in pivoted.columns:
            pivoted[col_name] = 0.0
            
    # Select and order columns 1-24
    ordered_cols = [f'pct_hourly_{h:04d}' for h in range(1, 25)]
    pivoted = pivoted[ordered_cols]
    
    # Add pct_hourly_2500 column with 0
    pivoted['pct_hourly_2500'] = 0
    
    # Reset index to make dt_strata a column
    pivoted = pivoted.reset_index()
    
    # Add dow column back (it was lost in pivot)
    # We need to merge dow back or calculate it from dt_strata
    # Since dt_strata is unique per row in the pivoted table, we can map it
    # Create a mapping from dt_strata to dow
    dow_map = df[['dt_strata', 'dow']].drop_duplicates().set_index('dt_strata')['dow']
    pivoted['dow'] = pivoted['dt_strata'].map(dow_map)
    
    # Reorder columns to match target
    target_cols = ['dt_strata', 'dow'] + ordered_cols + ['pct_hourly_2500']
    result = pivoted[target_cols]
    
    # Ensure dtypes
    result['dow'] = result['dow'].astype('int64')
    result['pct_hourly_2500'] = result['pct_hourly_2500'].astype('int64')
    
    return result
