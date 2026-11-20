import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse date
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract features
    df['dt_strata'] = df['datetime'].dt.strftime('%m/%d/%y')
    df['dow'] = df['datetime'].dt.dayofweek + 1  # Monday=1, Sunday=7
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hour to target column name
    # Hour 0 -> 2400, Hour 1 -> 0100, ..., Hour 23 -> 2300
    def map_hour_to_col(h):
        if h == 0:
            return 'pct_hourly_2400'
        else:
            return f'pct_hourly_{h:02d}00'
            
    df['hour_col'] = df['hour'].apply(map_hour_to_col)
    
    # 4. Aggregate
    # Group by dt_strata and dow, sum zone_016 for each hour_col
    agg_df = df.groupby(['dt_strata', 'dow', 'hour_col'])['zone_016'].sum().reset_index()
    
    # 5. Pivot
    pivot_df = agg_df.pivot_table(index=['dt_strata', 'dow'], columns='hour_col', values='zone_016', fill_value=0.0)
    
    # 6. Ensure all 24 columns exist
    expected_cols = [f'pct_hourly_{h:02d}00' for h in range(1, 24)] + ['pct_hourly_2400']
    for col in expected_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0.0
            
    # 7. Reset index to make dt_strata and dow columns
    pivot_df = pivot_df.reset_index()
    
    # 8. Add pct_hourly_2500
    pivot_df['pct_hourly_2500'] = 0
    
    # 9. Select and order columns
    target_cols = ['dt_strata', 'dow'] + expected_cols + ['pct_hourly_2500']
    result = pivot_df[target_cols]
    
    # 10. Ensure dtypes
    result['dow'] = result['dow'].astype('int64')
    result['pct_hourly_2500'] = result['pct_hourly_2500'].astype('int64')
    
    # Convert float columns to float64
    for col in expected_cols:
        result[col] = result[col].astype('float64')
        
    return result
