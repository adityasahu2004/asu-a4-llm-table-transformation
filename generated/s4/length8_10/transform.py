import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    source = source.copy()
    source['Date'] = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    source['month'] = source['Date'].dt.month
    
    # Identify hourly columns (exclude Segment, Date, month)
    hour_cols = [c for c in source.columns if c not in ['Segment', 'Date', 'month']]
    
    # Melt to long format
    melted = pd.melt(
        source, 
        id_vars=['month'], 
        value_vars=hour_cols, 
        var_name='hour_label', 
        value_name='value'
    )
    
    # Extract hour integer from labels like '1:00', '10:00', '24:00:00'
    melted['hour'] = melted['hour_label'].str.split(':').str[0].astype(int)
    
    # Group by hour and month, calculate mean
    grouped = melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # Pivot to get months as columns
    pivoted = grouped.pivot(index='hour', columns='month', values='value').reset_index()
    
    # Rename month columns to lowercase full names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivoted.rename(columns=month_names, inplace=True)
    
    # Ensure column order matches target: hour, january, february, ...
    target_cols = ['hour'] + [month_names[i] for i in range(1, 13)]
    pivoted = pivoted[target_cols]
    
    # Sort by hour
    pivoted = pivoted.sort_values('hour').reset_index(drop=True)
    
    return pivoted
