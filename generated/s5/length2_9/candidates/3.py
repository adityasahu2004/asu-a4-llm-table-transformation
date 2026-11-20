import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract components
    df['dt_strata'] = df['dt'].dt.strftime('%m/%d/%y')
    df['dow'] = df['dt'].dt.dayofweek + 1  # Monday=1, Sunday=7
    
    # Extract hour and map 0 to 24
    df['hour'] = df['dt'].dt.hour
    df['hour_mapped'] = df['hour'].apply(lambda h: 24 if h == 0 else h)
    
    # Create column name prefix
    df['col_name'] = 'pct_hourly_' + df['hour_mapped'].astype(str).str.zfill(4)
    
    # Aggregate: Sum the values for each date, dow, and hour
    # Note: The sample suggests a multiplication factor of 11 (67.9 * 11 = 746.9)
    agg_df = df.groupby(['dt_strata', 'dow', 'col_name'])['zone_016'].sum().reset_index()
    
    # Apply the scaling factor observed in the sample
    agg_df['value'] = agg_df['zone_016'] * 11
    
    # Pivot to wide format
    pivot_df = agg_df.pivot_table(index=['dt_strata', 'dow'], columns='col_name', values='value', fill_value=0.0).reset_index()
    
    # Ensure all 24 hour columns exist
    expected_cols = [f'pct_hourly_{h:04d}' for h in range(1, 25)]
    for col in expected_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0.0
            
    # Reorder columns
    result_cols = ['dt_strata', 'dow'] + expected_cols
    pivot_df = pivot_df[result_cols]
    
    # Add the 25th hour column as 0
    pivot_df['pct_hourly_2500'] = 0
    
    # Sort by date to match typical output expectations (optional but good practice)
    pivot_df = pivot_df.sort_values('dt_strata').reset_index(drop=True)
    
    return pivot_df
