import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date string
    # Format observed: "7/28/2019 4:50" -> %m/%d/%Y %H:%M
    source = source.copy()
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    source['Hour'] = source['dt'].dt.hour
    source['Month'] = source['dt'].dt.month
    
    # 3. Group by Hour and Month, calculate mean of the measurement
    # The target has 24 rows (one per hour) and 12 columns (one per month).
    # We aggregate the logger value.
    agg_df = source.groupby(['Hour', 'Month'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot to wide format
    # Index: Hour, Columns: Month, Values: cerc_logger_1
    pivot_df = agg_df.pivot(index='Hour', columns='Month', values='cerc_logger_1')
    
    # 5. Rename month columns to full names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    pivot_df.rename(columns=month_names, inplace=True)
    
    # 6. Ensure all 24 hours are present (fill NaN if any hour is missing in source)
    # The target schema implies 24 distinct hours and 0 nulls. 
    # If source data is sparse, we might need to forward fill or assume complete data.
    # Given the "nulls: 0" in target, we assume the source covers all hours or we fill.
    # However, usually in these problems, if data is missing, it stays NaN unless specified.
    # But target says nulls: 0. Let's reindex to 0-23.
    all_hours = pd.RangeIndex(0, 24)
    pivot_df = pivot_df.reindex(all_hours)
    
    # If there are still NaNs (missing hours in source), we might need to handle them.
    # The problem statement says "Preserve NaNs unless the inferred operation requires otherwise."
    # But target schema says "nulls: 0". This implies the source has data for all hours.
    # We will not impute arbitrarily, but if reindex introduces NaNs, they are technically
    # required by the "24 rows" constraint. If the source doesn't have hour X, it's impossible
    # to have 0 nulls without imputation. Assuming source is complete for all hours.
    
    # 7. Reset index to make 'Hour' a column
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns={'index': 'Hour'}, inplace=True)
    
    # 8. Ensure column order matches target
    target_cols = ['Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    result = pivot_df[target_cols]
    
    # Ensure Hour is int64
    result['Hour'] = result['Hour'].astype('int64')
    
    return result
