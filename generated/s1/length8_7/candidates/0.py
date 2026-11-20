import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse Date
    source = source.copy()
    source['Date'] = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # 2. Melt the hour columns (1-24)
    # Identify hour columns
    hour_cols = [str(i) for i in range(1, 25)]
    
    # Melt
    long_df = source.melt(
        id_vars=['Date', 'Class'],
        value_vars=hour_cols,
        var_name='hour',
        value_name='value'
    )
    
    # 3. Convert hour to integer
    long_df['hour'] = long_df['hour'].astype(int)
    
    # 4. Extract month and map to name
    long_df['month_num'] = long_df['Date'].dt.month
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    long_df['month_name'] = long_df['month_num'].map(month_map)
    
    # 5. Aggregate: Mean value per hour and month
    agg_df = long_df.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 6. Pivot to wide format
    pivot_df = agg_df.pivot(index='hour', columns='month_name', values='value')
    
    # 7. Reset index and rename columns
    pivot_df = pivot_df.reset_index()
    
    # Ensure all month columns exist, even if empty in source
    all_months = ['january', 'february', 'march', 'april', 'may', 'june', 
                  'july', 'august', 'september', 'october', 'november', 'december']
    
    for m in all_months:
        if m not in pivot_df.columns:
            pivot_df[m] = np.nan
            
    # 8. Select and order columns
    result_cols = ['hour'] + all_months
    result_df = pivot_df[result_cols]
    
    # Ensure hour is int
    result_df['hour'] = result_df['hour'].astype(int)
    
    return result_df
