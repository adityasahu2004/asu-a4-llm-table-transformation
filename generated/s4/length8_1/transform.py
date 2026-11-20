import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format observed: "7/28/2019 4:50" -> %m/%d/%Y %H:%M
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract components
    df['Hour'] = df['dt'].dt.hour
    df['Month'] = df['dt'].dt.month
    
    # Pivot table: Index=Hour, Columns=Month, Values=Mean of cerc_logger_1
    # This aggregates across all years and days
    pivoted = df.pivot_table(
        index='Hour', 
        columns='Month', 
        values='cerc_logger_1', 
        aggfunc='mean'
    )
    
    # Rename months to English names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    pivoted.columns = [month_names[m] for m in pivoted.columns]
    
    # Reset index to make Hour a column
    result = pivoted.reset_index()
    
    # Ensure Hour is int
    result['Hour'] = result['Hour'].astype(int)
    
    # Sort by Hour to ensure 0-23 order
    result = result.sort_values('Hour').reset_index(drop=True)
    
    # Ensure column order matches target
    target_cols = ['Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    return result[target_cols]
