import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the Date column
    # Format: "Thu 10/01/2009" -> "%a %m/%d/%Y"
    source = source.copy()
    source['Date'] = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # 2. Identify hour columns
    # Columns are "1:00", "2:00", ..., "24:00:00"
    hour_cols = [c for c in source.columns if c not in ['Segment', 'Date']]
    
    # 3. Melt the DataFrame
    # We need to extract the hour integer from the column names
    # "1:00" -> 1, "24:00:00" -> 24
    def extract_hour(col_name):
        return int(col_name.split(':')[0])
    
    # Create a mapping for column names to hours
    col_to_hour = {col: extract_hour(col) for col in hour_cols}
    
    # Melt
    melted = pd.melt(
        source, 
        id_vars=['Date'], 
        value_vars=hour_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # Map column names to integer hours
    melted['hour'] = melted['hour_col'].map(col_to_hour)
    
    # 4. Extract month from Date
    melted['month'] = melted['Date'].dt.month
    
    # 5. Aggregate by hour and month
    # Sum the values
    aggregated = melted.groupby(['hour', 'month'])['value'].sum().reset_index()
    
    # 6. Pivot to wide format
    # Index: hour, Columns: month, Values: value
    pivoted = aggregated.pivot(index='hour', columns='month', values='value')
    
    # 7. Rename month columns to lowercase month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivoted.columns = [month_names.get(col, col) for col in pivoted.columns]
    
    # 8. Reset index to make hour a column
    result = pivoted.reset_index()
    
    # 9. Ensure column order matches target
    # Target: hour, january, february, ..., december
    target_cols = ['hour'] + [month_names[i] for i in range(1, 13)]
    result = result[target_cols]
    
    # 10. Sort by hour
    result = result.sort_values('hour').reset_index(drop=True)
    
    return result
