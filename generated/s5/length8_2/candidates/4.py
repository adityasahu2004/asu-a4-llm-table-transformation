import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract components
    df['Hour'] = df['datetime'].dt.hour
    df['Month'] = df['datetime'].dt.month
    df['Year'] = df['datetime'].dt.year
    
    # Aggregate by Year, Month, Hour to get a single value per hour-slot
    # Using mean to handle multiple samples per hour
    agg_df = df.groupby(['Year', 'Month', 'Hour'])['zone_016'].mean().reset_index()
    
    # We need to pivot such that rows are Hours and columns are Months.
    # Since the target has one row per Hour (0-23) and columns for each month,
    # we assume the data is consistent enough or we just take the latest/mean across years if needed.
    # However, looking at the target, it seems to imply a single snapshot or average profile.
    # Given the source has distinct dates, and target has 24 rows (one per hour),
    # we likely need to average across all years for each Month/Hour combination.
    
    # Group by Month and Hour and average zone_016
    profile_df = agg_df.groupby(['Month', 'Hour'])['zone_016'].mean().reset_index()
    
    # Pivot: Index=Hour, Columns=Month, Values=zone_016
    pivoted = profile_df.pivot(index='Hour', columns='Month', values='zone_016')
    
    # Ensure all months 1-12 are present
    all_months = list(range(1, 13))
    pivoted = pivoted.reindex(columns=all_months)
    
    # Rename columns to month names
    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    pivoted.columns = month_names
    
    # Reset index to make Hour a column
    result = pivoted.reset_index()
    
    # Ensure Hour is int
    result['Hour'] = result['Hour'].astype(int)
    
    # Sort by Hour
    result = result.sort_values('Hour').reset_index(drop=True)
    
    # Reorder columns: Hour first, then months
    cols = ['Hour'] + month_names
    result = result[cols]
    
    return result
