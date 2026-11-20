import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column to datetime
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Pivot the data: Index by date, Columns by hour, Values by cooling_sp
    # This creates a wide table with hours 0-23 as columns
    pivot_df = df.pivot_table(
        index='date_only', 
        columns='hour', 
        values='zone_016_cooling_sp'
    )
    
    # 4. Ensure all 24 hour columns exist (0-23)
    # Reindex to ensure columns 0-23 are present, filling missing with NaN
    pivot_df = pivot_df.reindex(columns=range(24), fill_value=np.nan)
    
    # 5. Rename columns to value1...value24
    pivot_df.columns = [f'value{i+1}' for i in range(24)]
    
    # 6. Filter rows where value11 to value22 are not null
    # The target schema indicates these columns have 0 nulls.
    # This implies the target only contains dates where these specific hours had data.
    cols_to_check = [f'value{i}' for i in range(11, 23)] # 11 to 22 inclusive
    pivot_df = pivot_df.dropna(subset=cols_to_check)
    
    # 7. Cast specific columns to int64
    # value11 to value22 are int64 in target
    for col in cols_to_check:
        pivot_df[col] = pivot_df[col].astype('int64')
        
    # value1-10 and 23-24 remain float64 (default from pivot)
    
    # 8. Reset index to make date a column
    pivot_df = pivot_df.reset_index()
    
    # 9. Format the date column to MM/DD/YYYY string
    pivot_df['date'] = pivot_df['date_only'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # 10. Select and order columns as per target
    # Target columns: date, value1...value24
    target_cols = ['date'] + [f'value{i}' for i in range(1, 25)]
    result = pivot_df[target_cols]
    
    # 11. Sort by date to ensure consistent ordering (optional but good practice)
    # The target sample isn't sorted, but standard output usually is. 
    # If strict order preservation is needed, we'd need to track original order.
    # Given the aggregation, sorting by date is the most logical deterministic output.
    result = result.sort_values('date').reset_index(drop=True)
    
    return result
