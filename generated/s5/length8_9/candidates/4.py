import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Identify hourly columns
    hour_cols = [c for c in source.columns if c.startswith('Hr ')]
    
    # Melt the dataframe to long format
    df = source[['Date'] + hour_cols].melt(
        id_vars=['Date'], 
        value_vars=hour_cols, 
        var_name='HourStr', 
        value_name='value'
    )
    
    # Parse Date and extract Month
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df['Month'] = df['Date'].dt.month
    
    # Extract Hour number from HourStr (e.g., "Hr 1" -> 1)
    df['Hour'] = df['HourStr'].str.extract(r'(\d+)').astype(int)
    
    # Group by Month and Hour, summing the values
    # Note: The target has 24 rows (one per hour) and 12 columns (one per month).
    # The values in the target sample appear to be sums of all rows in the source 
    # for that specific hour and month.
    grouped = df.groupby(['Month', 'Hour'])['value'].sum().reset_index()
    
    # Pivot to wide format
    pivoted = grouped.pivot(index='Hour', columns='Month', values='value')
    
    # Ensure all hours 1-24 are present
    pivoted = pivoted.reindex(range(1, 25))
    
    # Rename columns to month names
    month_names = [
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    pivoted.columns = month_names
    
    # Reset index to make 'hour' a column
    pivoted = pivoted.reset_index()
    pivoted.rename(columns={'index': 'hour'}, inplace=True)
    
    # Sort by hour
    pivoted = pivoted.sort_values('hour').reset_index(drop=True)
    
    return pivoted
