import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract Hour and Month
    df['Hour'] = df['dt'].dt.hour
    df['Month'] = df['dt'].dt.month
    
    # Filter for Cooling Season (Sep, Oct, Nov)
    # Based on target having data for Sep, Oct, Nov and NaN for others
    df_filtered = df[df['Month'].isin([9, 10, 11])]
    
    # Pivot to get Hour x Month matrix
    # Values are zone_016_cooling_sp
    pivot_df = df_filtered.pivot_table(
        index='Hour', 
        columns='Month', 
        values='zone_016_cooling_sp', 
        aggfunc='mean' # Mean/Mode/Median all same for constant 73.0
    )
    
    # Create a full index of 0-23
    full_index = pd.RangeIndex(0, 24)
    pivot_df = pivot_df.reindex(full_index)
    
    # Map month numbers to names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    
    # Rename columns
    pivot_df = pivot_df.rename(columns=month_names)
    
    # Ensure all month columns exist (for NaN months)
    for m in range(1, 13):
        if month_names[m] not in pivot_df.columns:
            pivot_df[month_names[m]] = np.nan
            
    # Sort columns by standard month order
    ordered_cols = [month_names[m] for m in range(1, 13)]
    pivot_df = pivot_df[ordered_cols]
    
    # Rename index to 'Hour'
    pivot_df.index.name = 'Hour'
    
    # Reset index to make 'Hour' a column
    result = pivot_df.reset_index()
    
    # Ensure Hour is int
    result['Hour'] = result['Hour'].astype(int)
    
    return result
