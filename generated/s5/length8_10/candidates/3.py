import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    source = source.copy()
    source['parsed_date'] = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    source['month'] = source['parsed_date'].dt.month
    
    # Identify hour columns (all float columns except potentially others, but here specifically 1:00 to 24:00:00)
    # The source has columns '1:00' through '23:00' and '24:00:00'.
    hour_cols = [c for c in source.columns if c not in ['Segment', 'Date', 'parsed_date', 'month']]
    
    # Melt the dataframe
    melted = pd.melt(
        source, 
        id_vars=['parsed_date', 'month'], 
        value_vars=hour_cols, 
        var_name='hour_label', 
        value_name='value'
    )
    
    # Extract hour integer from label
    # Labels are like "1:00", "2:00", ..., "24:00:00"
    def extract_hour(label):
        return int(label.split(':')[0])
    
    melted['hour'] = melted['hour_label'].apply(extract_hour)
    
    # Group by hour and month, calculate mean
    grouped = melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # Map month numbers to names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    grouped['month_name'] = grouped['month'].map(month_map)
    
    # Pivot to get months as columns
    pivoted = grouped.pivot(index='hour', columns='month_name', values='value').reset_index()
    
    # Ensure all month columns are present and in order
    month_order = [
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # Fill any missing months with NaN if necessary (though groupby should cover all present data)
    for m in month_order:
        if m not in pivoted.columns:
            pivoted[m] = np.nan
            
    # Select and order columns
    result = pivoted[['hour'] + month_order]
    
    return result
