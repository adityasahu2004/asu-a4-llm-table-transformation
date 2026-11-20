import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month_name'] = source['dt'].dt.month_name().str.lower()
    source['hour_num'] = source['dt'].dt.hour # This gives 0-23. We need 1-24 mapping based on AM/PM cols.
    
    # The source has columns like "1:00 AM", "12:00 PM".
    # Let's map them manually to 1-24.
    hour_map = {}
    # AM hours: 1-11
    for h in range(1, 12):
        hour_map[f"{h}:00 AM"] = h
    # 12:00 PM is 12
    hour_map["12:00 PM"] = 12
    # PM hours: 1-11 become 13-23
    for h in range(1, 12):
        hour_map[f"{h}:00 PM"] = h + 12
    # 12:00 AM is 24
    hour_map["12:00 AM"] = 24
    
    # Identify hour columns
    hour_cols = [c for c in source.columns if c in hour_map]
    
    # Melt
    long_df = source.melt(id_vars=['month_name'], value_vars=hour_cols, var_name='hour_label', value_name='value')
    long_df['hour'] = long_df['hour_label'].map(hour_map)
    long_df = long_df.dropna(subset=['hour']) # Should not happen if map is correct
    
    # Group by hour and month, calculate mean
    grouped = long_df.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # Pivot to wide
    result = grouped.pivot(index='hour', columns='month_name', values='value').reset_index()
    
    # Rename columns
    result.columns.name = None
    # Ensure all month columns exist, even if null
    all_months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    for m in all_months:
        if m not in result.columns:
            result[m] = np.nan
            
    # Select and order columns
    result = result[['hour'] + all_months]
    
    # Sort by hour
    result = result.sort_values('hour').reset_index(drop=True)
    
    return result
