import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse dates
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Extract month and daytype
    df['month'] = df['date'].dt.strftime('%B')
    # 0=Monday, ..., 5=Saturday, 6=Sunday
    df['daytype'] = np.where(df['date'].dt.dayofweek >= 5, 'weekend', 'weekday')
    
    # 3. Identify hourly columns
    # Exclude 'date', 'month', 'daytype', 'DSL'
    hourly_cols = [c for c in df.columns if c not in ['date', 'month', 'daytype', 'DSL']]
    
    # 4. Melt the dataframe
    melted = df.melt(
        id_vars=['date', 'month', 'daytype'],
        value_vars=hourly_cols,
        var_name='time_label',
        value_name='value'
    )
    
    # 5. Map time labels to hour indices (1-24)
    # Mapping based on standard 12-hour clock interpretation for hourly data
    # 12:00 AM is the first hour (1), 1:00 AM is second (2), etc.
    time_map = {
        '12:00 AM': 1,
        '1:00 AM': 2,
        '2:00 AM': 3,
        '3:00 AM': 4,
        '4:00 AM': 5,
        '5:00 AM': 6,
        '6:00 AM': 7,
        '7:00 AM': 8,
        '8:00 AM': 9,
        '9:00 AM': 10,
        '10:00 AM': 11,
        '11:00 AM': 12,
        '12:00 PM': 13,
        '1:00 PM': 14,
        '2:00 PM': 15,
        '3:00 PM': 16,
        '4:00 PM': 17,
        '5:00 PM': 18,
        '6:00 PM': 19,
        '7:00 PM': 20,
        '8:00 PM': 21,
        '9:00 PM': 22,
        '10:00 PM': 23,
        '11:00 PM': 24
    }
    
    melted['hour_idx'] = melted['time_label'].map(time_map)
    
    # 6. Pivot to wide format
    # We want month and daytype as rows, and hours as columns
    pivoted = melted.pivot_table(
        index=['month', 'daytype'],
        columns='hour_idx',
        values='value',
        aggfunc='mean' # In case of duplicates, though source seems unique per date
    )
    
    # 7. Reset index and rename columns
    pivoted = pivoted.reset_index()
    
    # Rename hour columns to hr1, hr2, ... hr24
    new_col_names = {}
    for col in pivoted.columns:
        if col in time_map.values():
            new_col_names[col] = f'hr{col}'
            
    pivoted.rename(columns=new_col_names, inplace=True)
    
    # 8. Ensure column order
    # Target order: month, daytype, hr1, hr2, ..., hr24
    ordered_cols = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    result = pivoted[ordered_cols]
    
    # 9. Sort by month (chronologically) and daytype
    # To sort months chronologically, we can map them to numbers or use a custom sort
    month_order = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
        'October': 10, 'November': 11, 'December': 12
    }
    result['month_num'] = result['month'].map(month_order)
    result = result.sort_values(by=['month_num', 'daytype']).drop(columns=['month_num']).reset_index(drop=True)
    
    return result
