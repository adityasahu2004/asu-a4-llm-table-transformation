import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates to get month
    dates = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    months = dates.dt.month
    
    # Select hourly columns
    hourly_cols = [f'PCT_HOURLY_{h:02d}00' for h in range(1, 25)]
    
    # Create a long format dataframe for easier grouping
    # We need to aggregate by Month and Hour
    # Since we want mean per month per hour, we can iterate or use melt
    
    # Melt the source dataframe for the hourly columns
    # Keep only the necessary columns for melting
    melt_df = source[hourly_cols].copy()
    melt_df['month'] = months.values
    
    # Melt
    long_df = melt_df.melt(id_vars=['month'], var_name='hour_col', value_name='value')
    
    # Extract hour number from column name like 'PCT_HOURLY_0100' -> 1
    long_df['hour'] = long_df['hour_col'].str.extract(r'(\d{4})').astype(int) // 100
    
    # Group by month and hour, compute mean
    grouped = long_df.groupby(['month', 'hour'])['value'].mean().reset_index()
    
    # Pivot to wide format: index=hour, columns=month, values=value
    pivot_df = grouped.pivot(index='hour', columns='month', values='value')
    
    # Rename columns to month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivot_df.rename(columns=month_names, inplace=True)
    
    # Reset index to make hour a column
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns={'hour': 'hour'}, inplace=True)
    
    # Ensure column order matches target: hour, january, february, ..., december
    target_cols = ['hour'] + [month_names[m] for m in range(1, 13)]
    result = pivot_df[target_cols]
    
    return result
