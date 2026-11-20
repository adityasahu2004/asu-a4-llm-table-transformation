import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    source = source.copy()
    source['dt'] = pd.to_datetime(source['date'])
    
    # Group by calendar day
    # We use floor('D') to get the start of the day for grouping
    source['date_day'] = source['dt'].dt.floor('D')
    
    # Extract hour
    source['hour'] = source['dt'].dt.hour
    
    # Pivot the data to get hourly averages for each day
    # Columns will be hours 0-23
    pivot_df = source.groupby(['date_day', 'hour'])['cerc_logger_1'].mean().unstack('hour')
    
    # Rename columns to match target format: 1:00, ..., 23:00, 24:00
    # Hour 0 becomes '24:00', others become 'H:00'
    pivot_df.columns = [f'{col}:00' if col != 0 else '24:00' for col in pivot_df.columns]
    
    # Reorder columns: 1:00 to 24:00
    # Construct the list of desired column names
    hour_cols = [f'{h}:00' for h in range(1, 24)] + ['24:00']
    
    # Ensure all columns exist (fill NaNs with 0 or keep NaN? Target has 0 nulls, so fillna(0) might be appropriate, 
    # but let's stick to preserving data structure first. The target sample shows no NaNs. 
    # Given "distinct" counts are high, missing hours might be filled with 0 or interpolated. 
    # However, standard pivot leaves NaN. Let's fillna(0) to match "nulls: 0" in target schema.)
    pivot_df = pivot_df[hour_cols].fillna(0)
    
    # Format the date index for the 'cst' column
    # Format: "Sat 07/20/2019" -> %a %m/%d/%Y
    pivot_df.index = pivot_df.index.strftime('%a %m/%d/%Y')
    
    # Reset index to make date a column
    result = pivot_df.reset_index()
    result = result.rename(columns={'date_day': 'cst'})
    
    return result
