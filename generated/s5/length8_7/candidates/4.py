import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    source['Date'] = pd.to_datetime(source['Date'])
    
    # Extract Month
    source['Month'] = source['Date'].dt.month
    
    # Define hour columns
    hour_cols = [str(i) for i in range(1, 25)]
    
    # Melt the dataframe
    # Keep Date and Month, melt the hour columns
    long_df = source.melt(
        id_vars=['Date', 'Month'],
        value_vars=hour_cols,
        var_name='Hour',
        value_name='Value'
    )
    
    # Convert Hour to int
    long_df['Hour'] = long_df['Hour'].astype(int)
    
    # Group by Month and Hour and calculate mean
    agg_df = long_df.groupby(['Month', 'Hour'])['Value'].mean().reset_index()
    
    # Pivot to wide format
    # Index: Hour, Columns: Month, Values: Mean
    pivot_df = agg_df.pivot(index='Hour', columns='Month', values='Value')
    
    # Define month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    # Ensure all months are present columns
    pivot_df = pivot_df.reindex(columns=range(1, 13), fill_value=np.nan)
    
    # Rename columns
    pivot_df.rename(columns=month_names, inplace=True)
    
    # Reset index to make Hour a column
    result = pivot_df.reset_index()
    result.rename(columns={'index': 'hour'}, inplace=True)
    
    # Ensure hour is int64
    result['hour'] = result['hour'].astype(int)
    
    # Sort by hour to ensure consistent order (optional but good practice)
    result = result.sort_values('hour').reset_index(drop=True)
    
    return result
