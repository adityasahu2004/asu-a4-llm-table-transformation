import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date and hour
    df['date_only'] = df['datetime'].dt.normalize()
    df['hour_idx'] = df['datetime'].dt.hour  # 0-23
    
    # Map hour_idx to Hour 1 - Hour 24
    # Hour 1 = 0, Hour 2 = 1, ..., Hour 24 = 23
    df['hour_label'] = 'Hour ' + (df['hour_idx'] + 1).astype(str)
    
    # Group by date_only and hour_label, aggregate mean
    # This handles multiple readings per hour
    grouped = df.groupby(['date_only', 'hour_label'])['cerc_logger_1'].mean().reset_index()
    
    # Pivot the table
    pivot_df = grouped.pivot(index='date_only', columns='hour_label', values='cerc_logger_1')
    
    # Ensure all 24 hours are present as columns, filling missing with NaN
    expected_hours = [f'Hour {i}' for i in range(1, 25)]
    pivot_df = pivot_df.reindex(columns=expected_hours)
    
    # Reset index to make date_only a column
    pivot_df = pivot_df.reset_index()
    
    # Rename date_only to date and format it
    pivot_df['date'] = pivot_df['date_only'].dt.strftime('%m/%d/%Y')
    
    # Drop the intermediate date_only column
    pivot_df = pivot_df.drop(columns=['date_only'])
    
    # Reorder columns to match target: date, Hour 1, ..., Hour 24
    final_cols = ['date'] + expected_hours
    pivot_df = pivot_df[final_cols]
    
    return pivot_df.reset_index(drop=True)
