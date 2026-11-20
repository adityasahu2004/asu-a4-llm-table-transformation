import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format observed: "7/28/2019 4:50" -> %m/%d/%Y %H:%M
    # Note: Single digit months/days/hours are possible.
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract month name and pad to 10 chars as per target distinct values
    # e.g., "August   "
    df['month'] = df['dt'].dt.strftime('%B').str.pad(10, side='right')
    
    # Determine daytype
    # 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    df['daytype'] = np.where(df['dt'].dt.dayofweek >= 5, 'weekend', 'weekday')
    
    # Map hour to 1-24
    # 0 -> 24, 1 -> 1, ..., 23 -> 23
    hour = df['dt'].dt.hour
    df['hr'] = np.where(hour == 0, 24, hour)
    
    # Pivot to get mean value for each hour per month/daytype
    # We group by month, daytype, and hr, then mean the value
    agg_df = df.groupby(['month', 'daytype', 'hr'])['cerc_logger_1'].mean().reset_index()
    
    # Pivot the table
    result = agg_df.pivot_table(index=['month', 'daytype'], columns='hr', values='cerc_logger_1').reset_index()
    
    # Rename columns to hr1, hr2, ... hr24
    # The pivot columns will be integers 1..24
    new_cols = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    result.columns = new_cols
    
    # Ensure all hr columns are present (fill NaN if any hour missing for a group)
    for i in range(1, 25):
        if f'hr{i}' not in result.columns:
            result[f'hr{i}'] = np.nan
            
    # Sort columns to ensure order
    result = result[new_cols]
    
    return result
