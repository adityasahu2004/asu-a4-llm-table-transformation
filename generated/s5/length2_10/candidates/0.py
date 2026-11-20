import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format in source: "m/d/Y H:MM" or "m/d/Y H:MM"
    # Example: "11/6/2018 21:45"
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Identify cooling intervals (SP = 84.0)
    # Assuming 84.0 is "On" and 73.0 is "Off" based on the 876/0/657 pattern
    # 876 / 4 intervals = 219 per interval
    df['is_cooling'] = (df['zone_016_cooling_sp'] == 84.0).astype(int)
    
    # Determine hour bin (1-24)
    # Convention: 0:00-0:59 -> 24, 1:00-1:59 -> 1, ..., 23:00-23:59 -> 23
    df['hour_bin'] = df['dt'].apply(lambda x: 24 if x.hour == 0 else x.hour)
    
    # Group by Date and Hour Bin, sum the cooling indicators
    # We need to group by the date part only
    df['date_only'] = df['dt'].dt.date
    
    # Aggregate
    agg_df = df.groupby(['date_only', 'hour_bin'])['is_cooling'].sum().reset_index()
    
    # Calculate the metric: Count * 219
    agg_df['value'] = agg_df['is_cooling'] * 219
    
    # Pivot to wide format
    # Columns should be pct_hourly_0100 ... pct_hourly_2400
    pivot_df = agg_df.pivot(index='date_only', columns='hour_bin', values='value')
    
    # Ensure all hours 1-24 are present and fill with 0
    all_hours = range(1, 25)
    pivot_df = pivot_df.reindex(columns=all_hours, fill_value=0)
    
    # Rename columns to match target
    pivot_df.columns = [f'pct_hourly_{h:02d}00' for h in all_hours]
    
    # Convert index to datetime for dow calculation
    pivot_df.index = pd.to_datetime(pivot_df.index)
    
    # Calculate dow: Sunday=0, Monday=1, ..., Saturday=6
    # pandas dayofweek: Mon=0, ..., Sun=6
    # We want Sun=0. So (dayofweek + 1) % 7
    # Mon(0)->1, Tue(1)->2, ..., Sat(5)->6, Sun(6)->0
    pivot_df['dow'] = (pivot_df.index.dayofweek + 1) % 7
    
    # Format dt_strata as MM/DD/YY
    pivot_df['dt_strata'] = pivot_df.index.strftime('%m/%d/%y')
    
    # Add pct_hourly_2500 = 0
    pivot_df['pct_hourly_2500'] = 0
    
    # Select and order columns
    cols = ['dt_strata', 'dow'] + [f'pct_hourly_{h:02d}00' for h in range(1, 26)]
    
    # Ensure integer types for hourly columns
    for col in cols[2:]:
        pivot_df[col] = pivot_df[col].astype(int)
    pivot_df['dow'] = pivot_df['dow'].astype(int)
    
    result = pivot_df[cols].reset_index(drop=True)
    
    return result
