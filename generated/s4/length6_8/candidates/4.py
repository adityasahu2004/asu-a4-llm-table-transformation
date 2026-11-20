import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date and hour
    df['date_only'] = df['dt'].dt.date
    df['hour_bucket'] = df['dt'].dt.hour
    
    # Aggregate by date and hour bucket. 
    # Assuming mean aggregation for sensor data within the hour.
    agg_df = df.groupby(['date_only', 'hour_bucket'])['cerc_logger_1'].mean().reset_index()
    
    # Pivot to wide format
    # hour_bucket 0 -> Hr 1, 1 -> Hr 2, ..., 23 -> Hr 24
    pivoted = agg_df.pivot_table(index='date_only', columns='hour_bucket', values='cerc_logger_1')
    
    # Reindex to ensure all 24 hours are present (0-23)
    pivoted = pivoted.reindex(columns=range(24), fill_value=np.nan)
    
    # Rename columns to Hr 1, Hr 2, ... Hr 24
    pivoted.columns = [f'Hr {h+1}' for h in range(24)]
    
    # Format the date index to MM/DD/YYYY string
    pivoted.index = pivoted.index.astype(str) # Convert date object to string first if needed, but pd.date_range helps
    # Actually, date_only is a date object. We can format it.
    pivoted.index = pd.to_datetime(pivoted.index).strftime('%m/%d/%Y')
    
    # Reset index to make 'Date' a column
    result = pivoted.reset_index()
    result = result.rename(columns={'index': 'Date'})
    
    # Sort by Date to match typical chronological output (optional but good practice)
    # The target sample isn't strictly sorted (05/08/2019, 07/13/2019, 07/09/2018...), 
    # but usually, we preserve input order or sort. 
    # Since we grouped, we lost the original row order. 
    # The target distinct count is 521. 
    # Let's just return the pivoted data.
    
    return result
