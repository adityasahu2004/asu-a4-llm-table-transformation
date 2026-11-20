import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the date column
    # Format in source: "1/2/2018 0:11" -> M/D/YYYY H:MM
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M', errors='coerce')
    
    # Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Filter out rows where parsing failed
    df = df.dropna(subset=['datetime'])
    
    # Prepare for pivoting
    # We need to map hour 0 -> value1, hour 1 -> value2, ..., hour 23 -> value24
    # Create a column for the target column name
    df['col_name'] = 'value' + (df['hour'] + 1).astype(str)
    
    # Pivot the table
    # Index: date_only, Columns: col_name, Values: zone_016
    pivot_df = df.pivot_table(index='date_only', columns='col_name', values='zone_016', aggfunc='first')
    
    # Reset index to make date_only a column
    pivot_df = pivot_df.reset_index()
    
    # Rename the date column to 'date'
    pivot_df = pivot_df.rename(columns={'date_only': 'date'})
    
    # Format the date column as MM/DD/YYYY
    pivot_df['date'] = pd.to_datetime(pivot_df['date']).dt.strftime('%m/%d/%Y')
    
    # Ensure all value columns 1-24 exist, even if empty
    expected_cols = [f'value{i}' for i in range(1, 25)]
    
    # Reindex columns to ensure order and presence
    # Keep 'date' first, then the value columns
    final_cols = ['date'] + expected_cols
    
    # Select only the expected columns, filling missing ones with NaN
    pivot_df = pivot_df.reindex(columns=final_cols)
    
    # Sort by date descending as per target sample (01/02/2018 before 01/01/2018)
    # Convert back to datetime for sorting, then format again if necessary, 
    # but since we formatted to string, we can sort by the string if format is consistent,
    # or convert back. Let's convert back to datetime for safe sorting.
    pivot_df['date_dt'] = pd.to_datetime(pivot_df['date'])
    pivot_df = pivot_df.sort_values(by='date_dt', ascending=False)
    pivot_df = pivot_df.drop(columns=['date_dt'])
    
    # Reset index to clean up
    pivot_df = pivot_df.reset_index(drop=True)
    
    return pivot_df
