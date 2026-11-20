import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse Date and extract month
    source = source.copy()
    source['dt'] = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    source['month'] = source['dt'].dt.month
    
    # 2. Melt the hourly columns
    # Identify hourly columns
    hour_cols = [f'Hr {i}' for i in range(1, 25)]
    
    melted = source.melt(
        id_vars=['month'], 
        value_vars=hour_cols, 
        var_name='hour_str', 
        value_name='value'
    )
    
    # Extract hour number from 'Hr 1' -> 1
    melted['hour'] = melted['hour_str'].str.extract(r'(\d+)').astype(int)
    
    # 3. Group by hour and month, sum the values
    # Note: The target sample shows sums (e.g., Jan Hour 1 is ~721, source has ~2.4 per row, 2190 rows / 6 rates / 365 days ~ 1 row per rate per day? 
    # Actually, source has 2190 rows. 365 days * 6 rates = 2190. So each day/rate combo is unique.
    # The target has 24 rows (hours). The values are sums across all days in that month for that hour.
    agg_df = melted.groupby(['hour', 'month'])['value'].sum().reset_index()
    
    # 4. Pivot to wide format
    pivot_df = agg_df.pivot(index='hour', columns='month', values='value')
    
    # 5. Rename columns to month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivot_df.rename(columns=month_names, inplace=True)
    
    # Reset index to make 'hour' a column
    pivot_df = pivot_df.reset_index()
    
    # Ensure hour is int
    pivot_df['hour'] = pivot_df['hour'].astype(int)
    
    # Sort by hour to ensure order 1-24
    pivot_df = pivot_df.sort_values('hour').reset_index(drop=True)
    
    return pivot_df
