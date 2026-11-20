import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse date
    source = source.copy()
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month'] = source['dt'].dt.month
    
    # 2. Define hour mapping
    hour_map = {
        '1:00 AM': 1,
        '2:00 AM': 2,
        '3:00 AM': 3,
        '4:00 AM': 4,
        '5:00 AM': 5,
        '6:00 AM': 6,
        '7:00 AM': 7,
        '8:00 AM': 8,
        '9:00 AM': 9,
        '10:00 AM': 10,
        '11:00 AM': 11,
        '12:00 PM': 12,
        '1:00 PM': 13,
        '2:00 PM': 14,
        '3:00 PM': 15,
        '4:00 PM': 16,
        '5:00 PM': 17,
        '6:00 PM': 18,
        '7:00 PM': 19,
        '8:00 PM': 20,
        '9:00 PM': 21,
        '10:00 PM': 22,
        '11:00 PM': 23,
        '12:00 AM': 24
    }
    
    # 3. Melt the dataframe
    # Identify hour columns
    hour_cols = [c for c in source.columns if c in hour_map]
    
    melted = source.melt(
        id_vars=['dt', 'month'], 
        value_vars=hour_cols, 
        var_name='hour_label', 
        value_name='value'
    )
    
    # Map labels to integers
    melted['hour'] = melted['hour_label'].map(hour_map)
    
    # 4. Aggregate by hour and month
    # Calculate mean for each hour-month combination
    agg_df = melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 5. Pivot to wide format
    pivot_df = agg_df.pivot(index='hour', columns='month', values='value')
    
    # 6. Rename columns to month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivot_df.columns = [month_names.get(col, col) for col in pivot_df.columns]
    
    # Reset index to make 'hour' a column
    pivot_df = pivot_df.reset_index()
    
    # Ensure hour is int64
    pivot_df['hour'] = pivot_df['hour'].astype('int64')
    
    # Sort by hour for deterministic output
    pivot_df = pivot_df.sort_values('hour').reset_index(drop=True)
    
    return pivot_df
