import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract Hour and Month
    df['Hour'] = df['datetime'].dt.hour
    df['Month'] = df['datetime'].dt.month
    
    # Group by Hour and Month, and calculate the mean of zone_016
    # We use mean as it's the standard aggregation for this type of "typical day" profile
    agg_df = df.groupby(['Hour', 'Month'])['zone_016'].mean().reset_index()
    
    # Pivot the data to have Months as columns
    # The target has specific month names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    
    # Create a mapping for the pivot
    agg_df['Month_Name'] = agg_df['Month'].map(month_names)
    
    # Pivot
    pivot_df = agg_df.pivot(index='Hour', columns='Month_Name', values='zone_016')
    
    # Ensure all 24 hours are present
    all_hours = pd.RangeIndex(0, 24)
    pivot_df = pivot_df.reindex(all_hours)
    
    # Rename columns to match target exactly (Month names)
    # The pivot columns are already the month names
    
    # Reset index to make Hour a column
    result = pivot_df.reset_index()
    result = result.rename(columns={'index': 'Hour'})
    
    # Ensure Hour is int64
    result['Hour'] = result['Hour'].astype('int64')
    
    # Ensure column order matches target: Hour, Jan, Feb, ...
    target_cols = ['Hour'] + [month_names[i] for i in range(1, 13)]
    result = result[target_cols]
    
    return result
