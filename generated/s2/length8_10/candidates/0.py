import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    source = source.copy()
    source['dt'] = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    source['month'] = source['dt'].dt.month
    
    # Identify hourly columns
    hour_cols = [c for c in source.columns if c not in ['Segment', 'Date', 'dt', 'month']]
    
    # Melt to long format
    long_df = source.melt(
        id_vars=['month'], 
        value_vars=hour_cols, 
        var_name='hour_str', 
        value_name='value'
    )
    
    # Extract hour integer from hour_str
    # Examples: "1:00", "10:00", "24:00:00"
    long_df['hour'] = long_df['hour_str'].apply(lambda x: int(x.split(':')[0]))
    
    # Group by hour and month, calculate mean
    grouped = long_df.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # Pivot to wide format
    pivoted = grouped.pivot(index='hour', columns='month', values='value')
    
    # Rename columns to month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivoted.columns = [month_names[m] for m in pivoted.columns]
    
    # Reset index and rename index column to 'hour'
    result = pivoted.reset_index()
    result = result.rename(columns={'index': 'hour'})
    
    # Sort by hour
    result = result.sort_values('hour').reset_index(drop=True)
    
    return result
