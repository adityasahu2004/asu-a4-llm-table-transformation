import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse dates to extract month
    source = source.copy()
    source['DT_STRATA'] = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    source['month'] = source['DT_STRATA'].dt.month
    
    # 2. Identify hourly columns (0100 to 2400)
    # The source has PCT_HOURLY_0100 ... PCT_HOURLY_2400 and PCT_HOURLY_2500
    # We only want 0100-2400.
    hourly_cols = [col for col in source.columns if col.startswith('PCT_HOURLY_') and col != 'PCT_HOURLY_2500']
    
    # 3. Melt the dataframe
    # Extract hour from column name: PCT_HOURLY_0100 -> 1
    def get_hour(col_name):
        # Extract the last 4 digits
        hour_str = col_name.split('_')[-1]
        return int(hour_str)
    
    # Create a mapping for column names to hours
    col_to_hour = {col: get_hour(col) for col in hourly_cols}
    
    # Melt
    melted = source.melt(
        id_vars=['month'], 
        value_vars=hourly_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # Map column names to integer hours
    melted['hour'] = melted['hour_col'].map(col_to_hour)
    
    # 4. Group by hour and month, calculate mean
    # The target seems to be the average percentage for each hour across all strata/days in that month
    agg_df = melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 5. Pivot to wide format
    # Index: hour, Columns: month, Values: mean value
    pivoted = agg_df.pivot(index='hour', columns='month', values='value')
    
    # 6. Rename month columns to lowercase month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivoted.rename(columns=month_names, inplace=True)
    
    # 7. Reset index and ensure correct column order and types
    pivoted.reset_index(inplace=True)
    
    # Ensure hour is int
    pivoted['hour'] = pivoted['hour'].astype(int)
    
    # Sort by hour
    pivoted.sort_values('hour', inplace=True)
    pivoted.reset_index(drop=True, inplace=True)
    
    # Select only the required columns in the correct order
    target_cols = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                   'july', 'august', 'september', 'october', 'november', 'december']
    
    result = pivoted[target_cols]
    
    return result
