import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['parsed_dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    df['date_only'] = df['parsed_dt'].dt.strftime('%m/%d/%Y')
    df['hour'] = df['parsed_dt'].dt.hour + 1  # 1-based hour
    
    # Pivot the data
    # index: date_only, columns: hour, values: zone_016_cooling_sp
    pivoted = df.pivot_table(index='date_only', columns='hour', values='zone_016_cooling_sp', aggfunc='first')
    
    # Reset index to make date a column
    pivoted = pivoted.reset_index()
    
    # Rename columns to "Hour X"
    pivoted.columns.name = None
    new_cols = ['date']
    for h in range(1, 25):
        if h in pivoted.columns:
            new_cols.append(f'Hour {h}')
        else:
            # If a hour column is missing (no data for any row), it might not be in pivoted columns
            # However, pivot_table usually keeps all columns from the 'columns' arg if observed=False
            # Let's ensure we have all 24 hours if possible, or just rename existing
            pass
            
    # Re-index to ensure all hours 1-24 are present if they were in the source hours
    # The source has specific times, not necessarily every hour.
    # The target has 24 columns. We need to ensure columns 1-24 exist.
    
    # Let's rebuild the dataframe with explicit columns 1-24
    result = pd.DataFrame(pivoted['date'])
    for h in range(1, 25):
        if h in pivoted.columns:
            result[f'Hour {h}'] = pivoted[h]
        else:
            # If the hour doesn't exist in the pivoted data, it means no data for any day.
            # In the target, these columns still exist.
            # We need to determine the dtype. 
            # Looking at the target, hours 10-21 are int64, others float64.
            # This suggests hours 10-21 have no NaNs in the target eval set, while others do.
            # Since we can't know the eval set, we should just create the column with NaNs if missing.
            # But wait, the source has ~15k rows. It's likely sparse.
            # If a column is completely missing from pivot, it implies no data ever.
            # Let's assume we just take what's pivoted.
            # However, the target schema explicitly lists 24 columns.
            # If a column is missing from pivot, we must add it.
            result[f'Hour {h}'] = np.nan

    # The target shows specific dtypes. 
    # Hours 1-9, 22-24 are float64. Hours 10-21 are int64.
    # This pattern usually emerges if hours 10-21 have no nulls in the final result, 
    # while others have nulls.
    # We will not force cast to int64 if there are nulls, as that's invalid in pandas without nullable int types.
    # The target description says "int64" but allows "nulls: 0" for those columns.
    # If our result has nulls, it will be float64. If it has no nulls, it might be float64 or int64 depending on source.
    # We will return the result as is, allowing pandas to infer dtypes.
    
    return result
