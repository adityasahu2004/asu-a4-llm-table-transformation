import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date string into datetime
    # Source format: "7/28/2019 4:50" -> %m/%d/%Y %I:%M or %H:%M depending on AM/PM, 
    # but looking at samples: "4:50", "9:30", "18:50". It uses 24h format.
    # Format: %m/%d/%Y %H:%M
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date for grouping and hour for pivoting
    df['date_key'] = df['dt'].dt.date
    df['hour'] = df['dt'].dt.hour
    
    # Pivot table: Index=date_key, Columns=hour, Values=cerc_logger_1
    # We want columns 1-24 corresponding to hours 0-23
    pivot_df = df.pivot_table(
        index='date_key', 
        columns='hour', 
        values='cerc_logger_1', 
        aggfunc='first' # or mean, but usually unique per hour
    )
    
    # Rename columns from hour integers (0-23) to value1-value24
    pivot_df.columns = [f"value{h+1}" for h in pivot_df.columns]
    
    # Reset index to make date a column
    result = pivot_df.reset_index()
    
    # Format the date column as MM/DD/YYYY
    result['date'] = result['date_key'].apply(lambda x: x.strftime('%m/%d/%Y') if pd.notnull(x) else None)
    
    # Drop the temporary date_key column if it still exists (reset_index might keep it as 'date_key')
    if 'date_key' in result.columns:
        result = result.drop(columns=['date_key'])
    
    # Ensure correct column order
    target_cols = ['date'] + [f"value{i}" for i in range(1, 25)]
    result = result[target_cols]
    
    # Sort by date to match typical target presentation (optional but good practice)
    # The target sample shows dates not strictly sorted, but distinct count is 521.
    # We will just return the dataframe.
    
    return result
