import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    source = source.copy()
    source['date_dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month_name'] = source['date_dt'].dt.month_name().str.lower()
    
    # Define column to hour mapping
    col_map = {}
    # AM hours
    for h in range(1, 12):
        col_map[f'{h}:00 AM'] = h
    # 12 AM is 24
    col_map['12:00 AM'] = 24
    # PM hours
    col_map['12:00 PM'] = 12
    for h in range(1, 12):
        col_map[f'{h}:00 PM'] = 12 + h
        
    # Melt the dataframe
    # Select only the hour columns
    hour_cols = [c for c in source.columns if c in col_map]
    melted = source.melt(id_vars=['month_name'], value_vars=hour_cols, var_name='time_col', value_name='value')
    melted['hour'] = melted['time_col'].map(col_map)
    
    # Drop rows with NaN values if any (though source says 0 nulls for these cols)
    melted = melted.dropna(subset=['value'])
    
    # Group by hour and month, calculate mean
    grouped = melted.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # Pivot to wide format
    pivoted = grouped.pivot(index='hour', columns='month_name', values='value')
    
    # Ensure all 12 months are columns
    all_months = ['january', 'february', 'march', 'april', 'may', 'june', 
                  'july', 'august', 'september', 'october', 'november', 'december']
    
    for m in all_months:
        if m not in pivoted.columns:
            pivoted[m] = np.nan
            
    # Reorder columns
    pivoted = pivoted[all_months]
    
    # Reset index and rename
    pivoted = pivoted.reset_index()
    pivoted = pivoted.rename(columns={'index': 'hour'})
    
    # Sort by hour
    pivoted = pivoted.sort_values('hour').reset_index(drop=True)
    
    return pivoted
