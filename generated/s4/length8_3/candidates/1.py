import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format is M/D/YYYY H:MM or MM/DD/YYYY H:MM
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # Extract Hour and Month
    source['Hour'] = source['dt'].dt.hour
    source['Month'] = source['dt'].dt.month
    
    # Pivot the table
    # Index: Hour, Columns: Month, Values: zone_016_cooling_sp
    # Using mean to aggregate if multiple entries exist for same Hour/Month
    pivot_df = source.pivot_table(index='Hour', columns='Month', values='zone_016_cooling_sp', aggfunc='mean')
    
    # Reindex to ensure all 24 hours (0-23) are present
    pivot_df = pivot_df.reindex(range(24))
    
    # Rename month columns to full names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    pivot_df = pivot_df.rename(columns=month_names)
    
    # Reset index to make Hour a column
    result = pivot_df.reset_index()
    
    # Rename 'Hour' index name to 'Hour' column name if necessary (pivot_table might name it differently)
    result = result.rename(columns={'Hour': 'Hour'})
    
    # Ensure correct column order: Hour, then months in order
    cols = ['Hour'] + [month_names[i] for i in range(1, 13)]
    result = result[cols]
    
    # Ensure Hour is int64
    result['Hour'] = result['Hour'].astype('int64')
    
    return result
