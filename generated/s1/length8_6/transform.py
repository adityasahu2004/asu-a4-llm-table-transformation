import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse dates
    source = source.copy()
    source['date'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # 2. Identify time columns
    # The time columns are all columns except 'date' and 'DSL' (if DSL is present)
    # Based on schema, columns are 'date', 'DSL', and 24 time columns.
    time_cols = [col for col in source.columns if col not in ['date', 'DSL']]
    
    # 3. Melt the dataframe
    melted = pd.melt(
        source, 
        id_vars=['date'], 
        value_vars=time_cols, 
        var_name='time_label', 
        value_name='value'
    )
    
    # 4. Extract hour from time_label
    def parse_hour(label):
        # label format: "1:00 AM", "12:00 PM", etc.
        parts = label.split(':')
        hour_str = parts[0]
        ampm = parts[1].strip()
        hour = int(hour_str)
        
        if ampm == 'AM':
            if hour == 12:
                return 0
            else:
                return hour
        else: # PM
            if hour == 12:
                return 12
            else:
                return hour + 12
                
    melted['hour'] = melted['time_label'].apply(parse_hour)
    
    # 5. Extract month from date
    melted['month'] = melted['date'].dt.month
    
    # 6. Aggregate: Mean value per hour and month
    aggregated = melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 7. Pivot to wide format
    # Index: hour, Columns: month, Values: value
    pivoted = aggregated.pivot(index='hour', columns='month', values='value')
    
    # 8. Ensure all 12 months are present in columns, filling with NaN if missing
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    # Reindex columns to ensure all 12 months are present
    all_months = list(range(1, 13))
    pivoted = pivoted.reindex(columns=all_months)
    
    # Rename columns to month names
    pivoted = pivoted.rename(columns=month_names)
    
    # Reset index to make 'hour' a column
    result = pivoted.reset_index()
    
    # Sort by hour to ensure deterministic order (optional but good practice)
    result = result.sort_values('hour').reset_index(drop=True)
    
    # Select and order columns as per target schema
    target_cols = ['hour'] + [month_names[i] for i in range(1, 13)]
    result = result[target_cols]
    
    return result
