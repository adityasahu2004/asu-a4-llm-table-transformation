import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date string
    # Format observed: "1/2/2018 0:11" -> %m/%d/%Y %H:%M
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # Extract Hour and Month
    source['Hour'] = source['dt'].dt.hour
    source['Month'] = source['dt'].dt.month
    
    # Filter out nulls in the value column
    clean_df = source.dropna(subset=['zone_016'])
    
    # Group by Hour and Month, and take the mean
    # This handles potential duplicates for the same hour/month
    grouped = clean_df.groupby(['Hour', 'Month'])['zone_016'].mean().reset_index()
    
    # Pivot the table
    # Index: Hour, Columns: Month, Values: zone_016
    pivot_df = grouped.pivot(index='Hour', columns='Month', values='zone_016')
    
    # Map month numbers to names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    pivot_df = pivot_df.rename(columns=month_map)
    
    # Ensure all 24 hours are present
    all_hours = pd.RangeIndex(0, 24)
    pivot_df = pivot_df.reindex(all_hours)
    
    # Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'index': 'Hour'})
    
    # Ensure column order matches target specification
    target_cols = [
        'Hour', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Select only existing columns in that order
    # Note: If a month is missing from source, it won't be in pivot_df columns.
    # We should ensure all month columns exist, even if empty/NaN
    for col in target_cols:
        if col != 'Hour' and col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    return pivot_df[target_cols]
