import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse date
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract features
    df['month'] = df['datetime'].dt.month
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Filter out nulls in the value column
    df_valid = df.dropna(subset=['zone_016_cooling_sp'])
    
    # 4. Pivot
    # We want Hours as index, Months as columns, Value as data
    pivoted = df_valid.pivot_table(
        index='hour', 
        columns='month', 
        values='zone_016_cooling_sp', 
        aggfunc='first' # Assuming unique or consistent values per hour/month
    )
    
    # 5. Reconstruct columns
    # Ensure all 12 months are present
    all_months = range(1, 13)
    pivoted = pivoted.reindex(columns=all_months)
    
    # Convert index to column
    pivoted = pivoted.reset_index()
    pivoted.rename(columns={'hour': 'Hour'}, inplace=True)
    
    # Rename month integers to full names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    pivoted.rename(columns=month_names, inplace=True)
    
    # 6. Sort by Hour
    pivoted = pivoted.sort_values('Hour').reset_index(drop=True)
    
    # Ensure Hour is int64
    pivoted['Hour'] = pivoted['Hour'].astype('int64')
    
    return pivoted
