import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date to get month
    source = source.copy()
    source['date_dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month'] = source['date_dt'].dt.month
    
    # Melt the hourly columns
    hour_cols = [f'Hour {i}' for i in range(1, 25)]
    melted = source.melt(
        id_vars=['month'],
        value_vars=hour_cols,
        var_name='hour_label',
        value_name='value'
    )
    
    # Extract hour integer
    melted['hour'] = melted['hour_label'].str.replace('Hour ', '').astype(int)
    
    # Aggregate: Mean value for each hour and month
    agg = melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # Pivot to wide format
    pivoted = agg.pivot(index='hour', columns='month', values='value')
    
    # Rename month columns to lowercase names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivoted = pivoted.rename(columns=month_names)
    
    # Reset index to make 'hour' a column
    result = pivoted.reset_index()
    result = result.rename(columns={'index': 'hour'})
    
    # Ensure correct column order: hour, then months 1-12
    cols = ['hour'] + [month_names[i] for i in range(1, 13)]
    result = result[cols]
    
    # Sort by hour
    result = result.sort_values('hour').reset_index(drop=True)
    
    return result
