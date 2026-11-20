import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse date
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Derive keys
    # Month name, padded to 10 characters to match target "August   ", etc.
    df['month'] = df['dt'].dt.strftime('%B').str.ljust(10)
    
    # Day type: 5=Sat, 6=Sun in pandas (Mon=0)
    df['daytype'] = np.where(df['dt'].dt.dayofweek.isin([5, 6]), 'weekend', 'weekday')
    
    # 3. Derive hour bucket index (1-24)
    # Source hour 0 -> Target hr24
    # Source hour 1 -> Target hr1
    # ...
    # Source hour 23 -> Target hr23
    hour = df['dt'].dt.hour
    df['hour_idx'] = np.where(hour == 0, 24, hour)
    
    # 4. Aggregate
    # Group by month, daytype, and hour_idx, then mean the value
    agg_df = df.groupby(['month', 'daytype', 'hour_idx'])['cerc_logger_1'].mean().reset_index()
    
    # 5. Pivot to wide format
    # Index: month, daytype
    # Columns: hour_idx
    # Values: cerc_logger_1
    pivot_df = agg_df.pivot_table(index=['month', 'daytype'], columns='hour_idx', values='cerc_logger_1')
    
    # 6. Clean up and rename columns
    pivot_df = pivot_df.reset_index()
    
    # Rename columns from integers to 'hr1', 'hr2', ..., 'hr24'
    new_cols = {}
    for col in pivot_df.columns:
        if isinstance(col, (int, np.integer)):
            new_cols[col] = f'hr{col}'
        else:
            new_cols[col] = col
            
    pivot_df.rename(columns=new_cols, inplace=True)
    
    # Ensure correct column order
    # Target order: month, daytype, hr1...hr24
    ordered_cols = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # Select only existing columns in case some hours are missing (though unlikely with full data)
    existing_cols = [c for c in ordered_cols if c in pivot_df.columns]
    result = pivot_df[existing_cols]
    
    return result
