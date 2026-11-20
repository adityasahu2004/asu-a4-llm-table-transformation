import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract features
    df['month_name'] = df['dt'].dt.strftime('%B')
    df['day_of_week'] = df['dt'].dt.dayofweek # 0=Mon, 6=Sun
    df['hour_1_based'] = df['dt'].dt.hour + 1 # 0->1, 23->24
    
    # Determine daytype
    df['daytype'] = np.where(df['day_of_week'] < 5, 'weekday', 'weekend')
    
    # Format month to match target distinct values (10 chars, left aligned/padded with spaces)
    # The target sample shows "August   ", "April    ", etc.
    df['month'] = df['month_name'].str.pad(10, side='right')
    
    # Group by month and daytype, and mean by hour
    # We need to pivot so that rows are (month, daytype) and cols are hr1..hr24
    
    # Create a temporary dataframe for pivoting
    pivot_df = df[['month', 'daytype', 'hour_1_based', 'cerc_logger_1']].copy()
    
    # Pivot table
    # index: month, daytype
    # columns: hour_1_based
    # values: cerc_logger_1
    # aggfunc: mean
    
    pivoted = pivot_df.pivot_table(
        index=['month', 'daytype'],
        columns='hour_1_based',
        values='cerc_logger_1',
        aggfunc='mean'
    )
    
    # Flatten columns if necessary (pivot_table might create MultiIndex columns)
    pivoted.columns = [f'hr{int(col)}' for col in pivoted.columns]
    
    # Reset index to make month and daytype columns
    result = pivoted.reset_index()
    
    # Ensure all hr1-hr24 columns exist, fill NaN if any hour is missing for a group
    for h in range(1, 25):
        col_name = f'hr{h}'
        if col_name not in result.columns:
            result[col_name] = np.nan
            
    # Sort columns to match target order: month, daytype, hr1, hr2, ...
    target_cols = ['month', 'daytype'] + [f'hr{h}' for h in range(1, 25)]
    result = result[target_cols]
    
    # Sort by month name alphabetically to match typical output, though target sample order is mixed.
    # The target sample isn't strictly sorted by month. However, standard practice is often sorted.
    # Looking at target distinct values: August, April, September, December, March, October, February, May, January, November, June, July.
    # This is alphabetical.
    result = result.sort_values('month').reset_index(drop=True)
    
    return result
