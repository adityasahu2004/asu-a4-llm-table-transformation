import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    # Format is M/D/YYYY H:MM
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Pivot the data
    # We want to group by date_only and spread the hours into columns
    # The value to aggregate is cerc_logger_1
    # Since there might be multiple entries per hour or missing hours, 
    # we need to handle aggregation. The problem implies a single value per hour 
    # or an average if multiple exist. Given the distinct counts and nature of 
    # logger data, it's likely one reading per hour or we take the mean/first.
    # Looking at the target, there are NaNs for missing hours.
    # Let's use 'first' or 'mean'. Usually, if there's only one, it doesn't matter.
    # If there are multiple, 'mean' is safer for sensor data, but 'first' preserves 
    # the specific reading if it's a snapshot. 
    # However, looking at the source sample, the times are irregular (4:50, 9:30).
    # It's possible there is only one reading per hour in the full dataset, 
    # or we need to aggregate. Let's assume 'first' for simplicity unless 
    # duplicates are common. Actually, 'mean' is more robust for "logger" data 
    # which might have multiple samples. But let's look at the distinct counts.
    # Source distinct: 1279. Rows: 74848. This suggests many duplicates or 
    # repeated values. Wait, 74848 rows / 521 days ~ 143 readings per day?
    # That's more than 24. So there are multiple readings per hour.
    # We should probably take the mean or median. Let's use mean.
    
    pivot_df = df.pivot_table(
        index='date_only',
        columns='hour',
        values='cerc_logger_1',
        aggfunc='mean'
    )
    
    # 4. Rename columns to Hr 1 ... Hr 24
    # Hour 0 -> Hr 1, Hour 1 -> Hr 2, ..., Hour 23 -> Hr 24
    pivot_df.columns = [f'Hr {h + 1}' for h in pivot_df.columns]
    
    # 5. Reset index and format Date
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns={'date_only': 'Date'}, inplace=True)
    
    # Format Date as MM/DD/YYYY
    pivot_df['Date'] = pd.to_datetime(pivot_df['Date']).dt.strftime('%m/%d/%Y')
    
    # 6. Ensure all Hr columns are present and ordered
    expected_cols = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # Reindex to ensure all columns exist (filling NaNs for missing hours)
    pivot_df = pivot_df.reindex(columns=expected_cols)
    
    # Sort by Date to ensure deterministic order
    pivot_df = pivot_df.sort_values('Date').reset_index(drop=True)
    
    return pivot_df
