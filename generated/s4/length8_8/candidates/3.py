import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date to extract month
    source = source.copy()
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month'] = source['dt'].dt.month
    
    # Identify hour columns
    hour_cols = [c for c in source.columns if c.startswith('Hour ')]
    
    # Melt to long format
    long_df = source.melt(
        id_vars=['month'], 
        value_vars=hour_cols, 
        var_name='hour_label', 
        value_name='value'
    )
    
    # Extract hour number
    long_df['hour'] = long_df['hour_label'].str.replace('Hour ', '', regex=False).astype(int)
    
    # Group by hour and month, taking the mean
    # Note: The target sample shows specific values that look like means or sums. 
    # Given the distinct values in target are few, and source has many rows per month,
    # aggregation is required. The target has 24 rows (one per hour).
    # Let's check the sample data. 
    # Source has 182 rows. Target has 24 rows.
    # The values in target for 'january' at hour 1 is 0.0002398657.
    # In source, all 'Hour 1' values are 0.0002398657. So mean is correct.
    # Hour 11 in january is 0.0. In source, Hour 11 is 0 for all rows.
    
    agg_df = long_df.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # Pivot
    pivot_df = agg_df.pivot(index='hour', columns='month', values='value').reset_index()
    
    # Rename columns to month names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivot_df.rename(columns=month_map, inplace=True)
    
    # Sort by hour
    pivot_df = pivot_df.sort_values('hour').reset_index(drop=True)
    
    # Ensure column order matches target: hour, january, ..., december
    target_cols = ['hour'] + [month_map[i] for i in range(1, 13)]
    pivot_df = pivot_df[target_cols]
    
    return pivot_df
