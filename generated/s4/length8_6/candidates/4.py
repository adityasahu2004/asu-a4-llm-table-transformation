import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse date
    source = source.copy()
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month_num'] = source['dt'].dt.month
    
    # 2. Define hour mapping for 12-hour format columns
    # Source columns: 1:00 AM ... 11:00 AM, 12:00 AM, 1:00 PM ... 11:00 PM, 12:00 PM
    # Target hours: 1-24
    
    # Identify hour columns (all float64 columns except DSL)
    hour_cols = [c for c in source.columns if c not in ['date', 'DSL', 'dt', 'month_num']]
    
    # Create a mapping dictionary
    hour_map = {}
    for col in hour_cols:
        if 'AM' in col:
            if '12:00' in col:
                h = 24
            else:
                h = int(col.split(':')[0])
        else: # PM
            if '12:00' in col:
                h = 12
            else:
                h = int(col.split(':')[0]) + 12
        hour_map[col] = h
        
    # 3. Melt the dataframe
    melted = pd.melt(source, 
                     id_vars=['month_num'], 
                     value_vars=hour_cols, 
                     var_name='time_col', 
                     value_name='val')
    
    # Map the time_col to integer hour
    melted['hour'] = melted['time_col'].map(hour_map)
    
    # 4. Aggregate by hour and month
    # We assume we want the mean of the values for that specific hour and month across all days
    agg_df = melted.groupby(['hour', 'month_num'])['val'].mean().reset_index()
    
    # 5. Pivot to wide format
    # Map month numbers to names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    agg_df['month_name'] = agg_df['month_num'].map(month_names)
    
    pivot_df = agg_df.pivot(index='hour', columns='month_name', values='val')
    
    # 6. Format output
    # Sort by hour
    pivot_df = pivot_df.sort_index()
    
    # Reset index to make 'hour' a column
    pivot_df = pivot_df.reset_index()
    
    # Rename 'hour' to match target if needed (it is 'hour')
    # Ensure all month columns exist, even if NaN
    expected_months = [
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    for m in expected_months:
        if m not in pivot_df.columns:
            pivot_df[m] = np.nan
            
    # Select and order columns
    result = pivot_df[['hour'] + expected_months]
    
    # Ensure hour is int64
    result['hour'] = result['hour'].astype('int64')
    
    return result
