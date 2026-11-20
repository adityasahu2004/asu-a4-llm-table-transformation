import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse Date
    source = source.copy()
    source['Date'] = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # 2. Melt the dataframe from wide to long
    # Identify hour columns
    hour_cols = [col for col in source.columns if col.startswith('Hr ')]
    
    melted = source.melt(
        id_vars=['Date'], 
        value_vars=hour_cols, 
        var_name='hour_str', 
        value_name='value'
    )
    
    # 3. Extract hour integer from column name 'Hr X'
    melted['hour'] = melted['hour_str'].str.extract(r'(\d+)').astype(int)
    
    # 4. Extract month from Date
    melted['month'] = melted['Date'].dt.month
    
    # 5. Aggregate: Sum values for each hour and month
    # We group by hour and month, then sum the values.
    # This sums across all days in that month for that specific hour,
    # and across all rates/companies if multiple exist for the same date/hour.
    aggregated = melted.groupby(['hour', 'month'])['value'].sum().reset_index()
    
    # 6. Pivot to wide format
    # Index: hour, Columns: month, Values: sum
    pivoted = aggregated.pivot(index='hour', columns='month', values='value')
    
    # 7. Rename month columns to lowercase names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivoted.rename(columns=month_names, inplace=True)
    
    # 8. Reset index to make 'hour' a column
    result = pivoted.reset_index()
    
    # 9. Ensure correct column order and types
    # The target schema specifies specific column order: hour, january, ..., december
    target_cols = ['hour'] + [month_names[i] for i in range(1, 13)]
    result = result[target_cols]
    
    # Ensure hour is int64
    result['hour'] = result['hour'].astype('int64')
    
    # Sort by hour to match typical output expectations (though pivot usually preserves order)
    result = result.sort_values('hour').reset_index(drop=True)
    
    return result
