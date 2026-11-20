import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'])
    df['date_key'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Pivot to get one row per date
    # Assume Hour 1 = 0:00, Hour 24 = 23:00
    # If there are multiple entries per date/hour, take the first/mean. 
    # Given the constant nature, first is safe.
    pivot_df = df.pivot_table(index='date_key', columns='hour', values='zone_016_cooling_sp', aggfunc='first')
    
    # Ensure all hours 0-23 exist
    for h in range(24):
        if h not in pivot_df.columns:
            pivot_df[h] = np.nan
            
    # Reorder and rename columns
    # Map 0->Hr 1, 1->Hr 2, ..., 23->Hr 24
    pivot_df = pivot_df.sort_index(axis=1)
    
    new_cols = [f'Hr {h+1}' for h in range(24)]
    pivot_df.columns = new_cols
    
    # Format date
    pivot_df.index = pivot_df.index.strftime('%m/%d/%Y')
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'date_key': 'Date'})
    
    return pivot_df
