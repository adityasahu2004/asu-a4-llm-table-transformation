import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date string
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # Create a DataFrame with datetime, date key, and value
    temp_df = pd.DataFrame({
        'date_dt': dt,
        'cerc_logger_1': source['cerc_logger_1']
    })
    
    # Extract date and hour
    temp_df['date_key'] = temp_df['date_dt'].dt.date
    temp_df['hour'] = temp_df['date_dt'].dt.hour
    
    # Map hour 0-23 to value1-value24
    # Hour 0 -> value1, Hour 1 -> value2, ..., Hour 23 -> value24
    temp_df['value_col'] = temp_df['hour'].apply(lambda h: f'value{h + 1}')
    
    # Pivot the table
    # Index: date_key, Columns: value_col, Values: cerc_logger_1
    pivoted = temp_df.pivot_table(
        index='date_key', 
        columns='value_col', 
        values='cerc_logger_1', 
        aggfunc='first' # Assuming unique hour per day, first is safe
    )
    
    # Ensure all 24 columns exist, even if some are missing (NaN)
    expected_cols = [f'value{i}' for i in range(1, 25)]
    pivoted = pivoted.reindex(columns=expected_cols)
    
    # Format the date index back to string MM/DD/YYYY
    pivoted.index = pd.to_datetime(pivoted.index).strftime('%m/%d/%Y')
    
    # Reset index to make 'date' a column
    result = pivoted.reset_index()
    result = result.rename(columns={'index': 'date'})
    
    # Sort by date to ensure chronological order if needed, though not strictly required by schema
    # The target sample seems sorted. Let's sort by date string (works for MM/DD/YYYY)
    result = result.sort_values('date').reset_index(drop=True)
    
    return result
