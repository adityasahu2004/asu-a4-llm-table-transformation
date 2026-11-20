import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'])
    
    # Extract date and hour
    df['cal_date'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Map hour to bucket 1-24
    # Hour 0 -> Hr 1
    # Hour 23 -> Hr 24
    df['bucket'] = df['hour'] + 1
    
    # Group by date and bucket, aggregate the value
    # Use mean to handle potential duplicates, or first if unique
    # The target shows single values, suggesting one value per bucket per day or averaging
    grouped = df.groupby(['cal_date', 'bucket'])['zone_016'].mean().reset_index()
    
    # Pivot
    pivoted = grouped.pivot(index='cal_date', columns='bucket', values='zone_016')
    
    # Ensure all buckets 1-24 are present
    all_buckets = range(1, 25)
    pivoted = pivoted.reindex(columns=all_buckets)
    
    # Rename columns to "Hr 1", "Hr 2", etc.
    pivoted.columns = [f'Hr {i}' for i in all_buckets]
    
    # Format date column
    pivoted.index = pivoted.index.strftime('%m/%d/%Y')
    pivoted = pivoted.reset_index()
    pivoted = pivoted.rename(columns={'cal_date': 'Date'})
    
    # Sort by Date descending as per target sample
    pivoted = pivoted.sort_values(by='Date', ascending=False).reset_index(drop=True)
    
    return pivoted
