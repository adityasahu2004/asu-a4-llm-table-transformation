import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract Hour and Month
    df['Hour'] = df['datetime'].dt.hour
    df['Month'] = df['datetime'].dt.month
    
    # Group by Hour and Month, calculate mean of zone_016
    # Using mean to aggregate multiple readings per hour/month
    agg_df = df.groupby(['Hour', 'Month'])['zone_016'].mean().reset_index()
    
    # Pivot the table: Index=Hour, Columns=Month, Values=zone_016
    pivot_df = agg_df.pivot(index='Hour', columns='Month', values='zone_016')
    
    # Rename month numbers to month names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    pivot_df.columns = [month_names.get(col, col) for col in pivot_df.columns]
    
    # Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # Ensure all month columns exist, even if empty/null
    for m_name in month_names.values():
        if m_name not in pivot_df.columns:
            pivot_df[m_name] = np.nan
            
    # Sort by Hour to ensure 0-23 order
    pivot_df = pivot_df.sort_values('Hour').reset_index(drop=True)
    
    # Select columns in the correct order: Hour, January, ..., December
    cols = ['Hour'] + [month_names[m] for m in range(1, 13)]
    result = pivot_df[cols]
    
    return result
