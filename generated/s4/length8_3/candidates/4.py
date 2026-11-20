import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse date and extract components
    source = source.copy()
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    source['Hour'] = source['dt'].dt.hour
    source['Month'] = source['dt'].dt.month
    
    # 2. Pivot the data
    # We need Hours 0-23 as rows and Months 1-12 as columns
    # Using 'first' to handle potential duplicates, though distinctness suggests unique timestamps
    pivot_df = source.pivot_table(
        index='Hour', 
        columns='Month', 
        values='zone_016_cooling_sp', 
        aggfunc='first'
    )
    
    # 3. Rename columns to month names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 
        5: 'May', 6: 'June', 7: 'July', 8: 'August', 
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    pivot_df = pivot_df.rename(columns=month_names)
    
    # 4. Ensure all hours 0-23 are present and sorted
    pivot_df = pivot_df.reindex(range(24)).reset_index()
    
    # 5. Rename index column to 'Hour'
    pivot_df = pivot_df.rename(columns={'index': 'Hour'})
    
    # 6. Ensure correct column order: Hour, then months Jan-Dec
    cols = ['Hour'] + [month_names[i] for i in range(1, 13)]
    pivot_df = pivot_df[cols]
    
    # 7. Ensure dtype of Hour is int64
    pivot_df['Hour'] = pivot_df['Hour'].astype('int64')
    
    return pivot_df
