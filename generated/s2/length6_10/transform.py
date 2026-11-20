import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date and hour
    df['Date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    df['Hour'] = df['datetime'].dt.hour
    
    # Pivot the data
    # Index: Date, Columns: Hour, Values: zone_016_cooling_sp
    pivoted = df.pivot_table(index='Date', columns='Hour', values='zone_016_cooling_sp', aggfunc='first')
    
    # Ensure all hours 0-23 are present
    all_hours = range(24)
    pivoted = pivoted.reindex(columns=all_hours)
    
    # Rename columns to Hr 1 ... Hr 24
    # Hour 0 -> Hr 1, Hour 1 -> Hr 2, ..., Hour 23 -> Hr 24
    pivoted.columns = [f'Hr {h+1}' for h in pivoted.columns]
    
    # Reset index to make Date a column
    result = pivoted.reset_index()
    
    return result
