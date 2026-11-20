import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    source['dt'] = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    source['month'] = source['dt'].dt.month
    
    # Identify hour columns (all except Segment, Date, dt, month)
    hour_cols = [c for c in source.columns if c not in ['Segment', 'Date', 'dt', 'month']]
    
    # Melt to long format
    long_df = pd.melt(
        source, 
        id_vars=['month'], 
        value_vars=hour_cols, 
        var_name='hour_str', 
        value_name='value'
    )
    
    # Extract hour integer from hour_str
    # Formats are "1:00", "12:00", "24:00:00"
    def extract_hour(h_str):
        return int(h_str.split(':')[0])
        
    long_df['hour'] = long_df['hour_str'].apply(extract_hour)
    
    # Group by hour and month, calculate mean
    grouped = long_df.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # Pivot to wide format
    pivoted = grouped.pivot(index='hour', columns='month', values='value').reset_index()
    
    # Rename month columns to lowercase month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    pivoted.rename(columns=month_names, inplace=True)
    
    # Ensure column order: hour, then months 1-12
    col_order = ['hour'] + [month_names[m] for m in range(1, 13)]
    
    return pivoted[col_order]
