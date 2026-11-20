import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date string
    # Format is M/d/yyyy H:mm (e.g., "1/2/2018 0:11")
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date part for grouping and hour for pivoting
    df['date_key'] = df['dt'].dt.date
    df['hour'] = df['dt'].dt.hour
    
    # Map hour 0-23 to Hr 1-24
    df['hr_label'] = 'Hr ' + (df['hour'] + 1).astype(str)
    
    # Pivot the table
    # Index: date_key, Columns: hr_label, Values: zone_016
    pivoted = df.pivot_table(index='date_key', columns='hr_label', values='zone_016', aggfunc='first')
    
    # Reset index to make date a column
    pivoted = pivoted.reset_index()
    
    # Rename date column
    pivoted = pivoted.rename(columns={'date_key': 'Date'})
    
    # Format Date as MM/DD/YYYY
    pivoted['Date'] = pd.to_datetime(pivoted['Date']).dt.strftime('%m/%d/%Y')
    
    # Ensure all Hr columns exist and are in order
    expected_cols = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # Reindex columns to ensure order and presence (missing hours will be NaN)
    pivoted = pivoted.reindex(columns=expected_cols)
    
    # Sort by Date descending as per target sample
    pivoted = pivoted.sort_values(by='Date', ascending=False).reset_index(drop=True)
    
    return pivoted
