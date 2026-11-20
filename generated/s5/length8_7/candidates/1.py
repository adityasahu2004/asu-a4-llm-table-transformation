import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse dates to extract month
    source = source.copy()
    source['dt'] = pd.to_datetime(source['Date'])
    source['month'] = source['dt'].dt.month
    
    # 2. Melt the hourly columns
    # Columns are named "1" through "24"
    hour_cols = [str(h) for h in range(1, 25)]
    melted = source.melt(
        id_vars=['dt', 'month'], 
        value_vars=hour_cols, 
        var_name='hour_str', 
        value_name='value'
    )
    
    # 3. Convert hour string to integer
    melted['hour'] = melted['hour_str'].astype(int)
    
    # 4. Group by hour and month, calculate mean
    aggregated = melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 5. Pivot to wide format: index=hour, columns=month, values=value
    pivoted = aggregated.pivot(index='hour', columns='month', values='value')
    
    # 6. Rename month columns to lowercase full names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivoted.rename(columns=month_names, inplace=True)
    
    # 7. Reset index to make hour a column
    result = pivoted.reset_index()
    
    # 8. Ensure hour is int64
    result['hour'] = result['hour'].astype('int64')
    
    # 9. Sort by hour to ensure deterministic order
    result = result.sort_values('hour').reset_index(drop=True)
    
    return result
