import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date for grouping and hour for pivoting
    df['date_key'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Pivot the data
    # Index: date_key, Columns: hour, Values: cerc_logger_1
    pivoted = df.pivot_table(index='date_key', columns='hour', values='cerc_logger_1')
    
    # Ensure all 24 hours are present (0-23)
    pivoted = pivoted.reindex(columns=range(24), fill_value=np.nan)
    
    # Rename columns: Hour 0 -> Hr 1, Hour 1 -> Hr 2, ..., Hour 23 -> Hr 24
    pivoted.columns = [f'Hr {h+1}' for h in range(24)]
    
    # Format the date index as MM/DD/YYYY
    pivoted.index = pivoted.index.strftime('%m/%d/%Y')
    
    # Reset index to make date a column
    result = pivoted.reset_index()
    result = result.rename(columns={'date_key': 'Date'})
    
    # Ensure column order matches target
    cols = ['Date'] + [f'Hr {h}' for h in range(1, 25)]
    result = result[cols]
    
    return result
