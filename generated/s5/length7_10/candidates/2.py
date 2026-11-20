import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format is M/D/YYYY H:MM
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract month name and pad to 10 chars to match target distinct values
    # e.g., "August   "
    df['month'] = df['datetime'].dt.strftime('%B').str.ljust(10)
    
    # Extract daytype: 0=Mon, 1=Tue, ..., 5=Sat, 6=Sun
    # Weekend if dayofweek is 5 or 6
    df['daytype'] = np.where(df['datetime'].dt.dayofweek.isin([5, 6]), 'weekend', 'weekday')
    
    # Extract hour (0-23)
    df['hour'] = df['datetime'].dt.hour
    
    # Group by month and daytype, then pivot by hour to get mean values
    # We need to aggregate because multiple records might exist for same month/daytype/hour
    # although the source looks like sparse time series, aggregation is safe.
    pivot_df = df.groupby(['month', 'daytype'])['cerc_logger_1'].apply(
        lambda x: x.groupby(df.loc[x.index, 'hour']).mean()
    ).unstack(level='hour', fill_value=np.nan)
    
    # Rename columns from hour index (0-23) to hr1-hr24
    # hour 0 -> hr1, hour 1 -> hr2, ..., hour 23 -> hr24
    pivot_df.columns = [f'hr{h+1}' for h in pivot_df.columns]
    
    # Reset index to make month and daytype columns
    result = pivot_df.reset_index()
    
    # Ensure column order matches target
    target_cols = ['month', 'daytype'] + [f'hr{h}' for h in range(1, 25)]
    result = result[target_cols]
    
    # Sort to ensure deterministic order if necessary, though groupby usually preserves order
    # The target sample seems sorted by month name or similar, but let's just return the grouped result.
    # To match the distinct_values order in target (August, April...), we might need specific sorting,
    # but typically just returning the grouped data is sufficient unless explicit sorting is inferred.
    # The target sample shows: August, October, January, November, October, August...
    # It's not strictly sorted. We will just return the aggregated result.
    
    return result.reset_index(drop=True)
