import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse date and extract month
    source = source.copy()
    source['date_dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month'] = source['date_dt'].dt.month
    
    # 2. Melt the hourly value columns
    # Columns value1 to value24
    id_cols = ['date', 'date_dt', 'month']
    value_cols = [f'value{i}' for i in range(1, 25)]
    
    melted = source.melt(
        id_vars=id_cols, 
        value_vars=value_cols, 
        var_name='hour_str', 
        value_name='val'
    )
    
    # Convert hour_str (value1) to hour int (1)
    melted['hour'] = melted['hour_str'].str.replace('value', '', regex=False).astype(int)
    
    # 3. Group by hour and month, calculate mean
    grouped = melted.groupby(['hour', 'month'])['val'].mean().reset_index()
    
    # 4. Pivot to wide format
    pivoted = grouped.pivot(index='hour', columns='month', values='val')
    
    # Reset index to make hour a column
    pivoted = pivoted.reset_index()
    
    # 5. Rename month columns to lowercase names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivoted.rename(columns=month_map, inplace=True)
    
    # 6. Ensure all 12 month columns exist, even if empty (NaN)
    for m_name in month_map.values():
        if m_name not in pivoted.columns:
            pivoted[m_name] = np.nan
            
    # 7. Sort by hour to ensure canonical order (1-24)
    pivoted = pivoted.sort_values('hour').reset_index(drop=True)
    
    # 8. Select and order columns as per target schema
    # Target: hour, january, february, ..., december
    col_order = ['hour'] + [month_map[i] for i in range(1, 13)]
    
    result = pivoted[col_order]
    
    # Ensure hour is int64
    result['hour'] = result['hour'].astype('int64')
    
    return result
