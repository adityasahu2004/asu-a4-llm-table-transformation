import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format in source: "m/d/Y H:M" e.g., "7/28/2019 4:50"
    source['datetime'] = pd.to_datetime(source['date'], format='%m/%d/%Y %I:%M%p', errors='coerce')
    # If the above fails due to 24h format in some entries or mixed, try generic
    if source['datetime'].isna().all():
        source['datetime'] = pd.to_datetime(source['date'], errors='coerce')
        
    # Extract date part formatted as MM/DD/YYYY
    source['date_fmt'] = source['datetime'].dt.strftime('%m/%d/%Y')
    
    # Extract hour (0-23)
    source['hour'] = source['datetime'].dt.hour
    
    # Prepare the pivot
    # We want columns value1 to value24 corresponding to hours 0 to 23
    # Create a column for the target column name
    source['col_name'] = 'value' + (source['hour'] + 1).astype(str)
    
    # Pivot the data
    # Index: date_fmt, Columns: col_name, Values: cerc_logger_1
    pivot_df = source.pivot_table(index='date_fmt', columns='col_name', values='cerc_logger_1', aggfunc='first')
    
    # Ensure all value columns 1-24 exist
    expected_cols = [f'value{i}' for i in range(1, 25)]
    for col in expected_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # Reorder columns
    pivot_df = pivot_df[expected_cols]
    
    # Reset index to make date a column
    result = pivot_df.reset_index()
    result = result.rename(columns={'date_fmt': 'date'})
    
    # Sort by date to match typical output expectations (optional but good practice)
    result = result.sort_values(by='date').reset_index(drop=True)
    
    return result
