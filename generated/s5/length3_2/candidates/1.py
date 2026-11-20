import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the datetime string
    source = source.copy()
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date for grouping and hour for pivoting
    source['date_key'] = source['dt'].dt.date
    source['hour'] = source['dt'].dt.hour
    
    # 3. Pivot the data
    # Rows: date_key, Cols: hour (0-23), Values: cerc_logger_1
    pivoted = source.pivot_table(
        index='date_key', 
        columns='hour', 
        values='cerc_logger_1', 
        aggfunc='first' # or 'mean' if duplicates exist, 'first' preserves the single value
    )
    
    # 4. Rename columns from 0-23 to "Hour 1" - "Hour 24"
    pivoted.columns = [f'Hour {h+1}' for h in pivoted.columns]
    
    # 5. Format the date index to MM/DD/YYYY
    pivoted.index = pivoted.index.strftime('%m/%d/%Y')
    
    # 6. Reset index to make date a column
    result = pivoted.reset_index()
    
    # Rename the index column to 'date'
    result = result.rename(columns={'date_key': 'date'})
    
    # Ensure column order matches target exactly
    # Target columns: date, Hour 1, ..., Hour 24
    cols = ['date'] + [f'Hour {h}' for h in range(1, 25)]
    result = result[cols]
    
    return result
