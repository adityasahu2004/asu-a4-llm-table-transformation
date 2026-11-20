import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse Date
    source = source.copy()
    source['parsed_date'] = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # 2. Extract Month Name
    # Map month number to lowercase name
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    source['month_name'] = source['parsed_date'].dt.month.map(month_names)
    
    # 3. Melt hourly columns
    # Identify hourly columns (1-24)
    hour_cols = [str(i) for i in range(1, 25)]
    
    melted = source.melt(
        id_vars=['month_name'], 
        value_vars=hour_cols, 
        var_name='hour_str', 
        value_name='value'
    )
    
    # Convert hour_str to int
    melted['hour'] = melted['hour_str'].astype(int)
    
    # 4. Aggregate
    # Group by hour and month_name, calculate mean
    aggregated = melted.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 5. Pivot
    # Pivot to get hours as rows, months as columns
    pivoted = aggregated.pivot_table(index='hour', columns='month_name', values='value')
    
    # 6. Ensure all month columns exist and order them
    all_months = [month_names[i] for i in range(1, 13)]
    
    # Reindex columns to ensure all months are present, filling missing with NaN
    pivoted = pivoted.reindex(columns=all_months)
    
    # 7. Reset index to make 'hour' a column
    result = pivoted.reset_index()
    
    # 8. Ensure 'hour' is int64
    result['hour'] = result['hour'].astype('int64')
    
    # 9. Select and order columns: hour + months
    final_cols = ['hour'] + all_months
    result = result[final_cols]
    
    return result
