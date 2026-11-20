import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date string
    # Format is like "1/2/2018 0:11" -> %m/%d/%Y %H:%M
    # Using infer_datetimeformat or mixed format handling if necessary, 
    # but standard strptime handles single digit months/days.
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour_0'] = df['datetime'].dt.hour
    
    # 3. Map hour 0-23 to 1-24
    df['hour_idx'] = df['hour_0'] + 1
    
    # 4. Pivot
    # We want dates as rows, hours as columns, values as zone_016
    pivoted = df.pivot_table(
        index='date_only', 
        columns='hour_idx', 
        values='zone_016', 
        aggfunc='first' # In case of duplicates, though likely unique per hour
    )
    
    # 5. Clean up and format
    pivoted = pivoted.reset_index()
    
    # Rename index column
    pivoted = pivoted.rename(columns={'date_only': 'date'})
    
    # Format date to MM/DD/YYYY
    pivoted['date'] = pd.to_datetime(pivoted['date']).dt.strftime('%m/%d/%Y')
    
    # Rename hour columns to "Hour X"
    new_cols = {}
    for col in pivoted.columns:
        if col != 'date':
            new_cols[col] = f'Hour {col}'
    pivoted = pivoted.rename(columns=new_cols)
    
    # Sort by date descending as per sample target (01/02/2018 first)
    pivoted = pivoted.sort_values(by='date', ascending=False).reset_index(drop=True)
    
    # Ensure column order matches target: date, then Hour 1 to Hour 24
    # The pivot creates columns in numerical order (1, 2, ... 24)
    # We just need to make sure they are present. If some hours are missing in data, they will be NaN.
    
    return pivoted
