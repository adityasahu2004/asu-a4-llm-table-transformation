import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    # Format observed: "7/28/2019 4:50" -> %m/%d/%Y %H:%M
    source = source.copy()
    source['datetime'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month Name
    source['Hour'] = source['datetime'].dt.hour
    # Map month number to name: 1->January, ..., 12->December
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    source['Month'] = source['datetime'].dt.month.map(month_names)
    
    # 3. Aggregate by Hour and Month
    # Calculate mean of cerc_logger_1
    agg_df = source.groupby(['Hour', 'Month'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot the data
    # Index: Hour, Columns: Month, Values: mean cerc_logger_1
    pivot_df = agg_df.pivot(index='Hour', columns='Month', values='cerc_logger_1')
    
    # 5. Format Output
    # Ensure all 24 hours are present, reindexing to 0-23
    all_hours = range(24)
    pivot_df = pivot_df.reindex(all_hours)
    
    # Ensure all month columns are present in calendar order
    expected_months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Reindex columns to ensure order and presence
    pivot_df = pivot_df.reindex(columns=expected_months)
    
    # Reset index to make Hour a column
    result = pivot_df.reset_index()
    
    # Rename the index column 'Hour' if it wasn't named correctly during reset_index
    # (reindex preserves name 'Hour' from the original groupby index)
    result.rename(columns={'Hour': 'Hour'}, inplace=True)
    
    # Ensure Hour is int64
    result['Hour'] = result['Hour'].astype('int64')
    
    # Select and order columns exactly as target
    final_columns = ['Hour'] + expected_months
    result = result[final_columns]
    
    return result
