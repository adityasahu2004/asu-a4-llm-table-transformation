import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse date and create a sortable datetime
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date string for grouping and final output
    df['date_only'] = df['dt'].dt.date
    
    # 3. Assign hourly sequence within each day
    # Sort by datetime to ensure correct chronological order for assignment
    df = df.sort_values('dt')
    
    # Group by date_only and assign 1-based rank
    df['hour_idx'] = df.groupby('date_only').cumcount() + 1
    
    # 4. Pivot the data
    # Index: date_only, Columns: hour_idx, Values: zone_016
    pivoted = df.pivot_table(index='date_only', columns='hour_idx', values='zone_016')
    
    # 5. Prepare output columns
    # Rename columns to value1, value2, ... value24
    pivoted.columns = [f'value{i}' for i in pivoted.columns]
    
    # Reset index to make date a column
    result = pivoted.reset_index()
    
    # Format date as MM/DD/YYYY
    result['date'] = result['date_only'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # Drop the helper date_only column
    result = result.drop(columns=['date_only'])
    
    # Ensure only value1-24 are present and in order
    expected_cols = ['date'] + [f'value{i}' for i in range(1, 25)]
    # Reindex to ensure all 24 value columns exist (filling NaNs if some hours are missing for a day)
    result = result.reindex(columns=expected_cols)
    
    # Sort by date descending as per target sample
    # Convert to datetime for sorting, then drop
    result['sort_key'] = pd.to_datetime(result['date'], format='%m/%d/%Y')
    result = result.sort_values('sort_key', ascending=False)
    result = result.drop(columns=['sort_key'])
    
    return result.reset_index(drop=True)
