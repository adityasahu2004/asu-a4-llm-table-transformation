import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the date column
    # Format in source: M/D/YYYY H:MM
    df['datetime'] = pd.to_datetime(df['date'])
    
    # Extract the date part (floor to day)
    df['date_only'] = df['datetime'].dt.floor('D')
    
    # Extract the hour (0-23)
    df['hour'] = df['datetime'].dt.hour
    
    # Map hour to target column names: value1 (hour 0) to value24 (hour 23)
    df['value_col'] = 'value' + (df['hour'] + 1).astype(str)
    
    # Group by date and value column, and aggregate the sensor value
    # Using mean as a robust aggregation for multiple readings per hour
    df_pivot = df.groupby(['date_only', 'value_col'])['cerc_logger_1'].mean()
    
    # Unstack to create columns for each value_col
    df_pivot = df_pivot.unstack(level='value_col')
    
    # Ensure all 24 value columns are present, filling missing with NaN
    expected_cols = [f'value{i}' for i in range(1, 25)]
    for col in expected_cols:
        if col not in df_pivot.columns:
            df_pivot[col] = np.nan
            
    # Select and order the columns
    df_pivot = df_pivot[expected_cols]
    
    # Reset index to make date_only a column
    df_pivot = df_pivot.reset_index()
    
    # Rename date_only to date
    df_pivot = df_pivot.rename(columns={'date_only': 'date'})
    
    # Format the date column to MM/DD/YYYY
    df_pivot['date'] = df_pivot['date'].dt.strftime('%m/%d/%Y')
    
    # Reorder columns to match target: date, value1, ..., value24
    final_cols = ['date'] + expected_cols
    result = df_pivot[final_cols]
    
    return result
