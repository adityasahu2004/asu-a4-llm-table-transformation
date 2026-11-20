import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    # Format: "M/D/YYYY H:MM"
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Pivot the data
    # We want rows as dates and columns as hours (1-24)
    # The target columns are "Hr 1" to "Hr 24"
    # Hour 0 -> Hr 1, Hour 1 -> Hr 2, ..., Hour 23 -> Hr 24
    
    # Create a pivot table
    # index: date_only, columns: hour, values: zone_016
    pivot_df = df.pivot_table(index='date_only', columns='hour', values='zone_016', aggfunc='first')
    
    # 4. Rename columns to "Hr 1", "Hr 2", ...
    # The columns in pivot_df are integers 0-23 (if present)
    # We need to ensure all 24 columns exist, even if NaN
    all_hours = range(24)
    pivot_df = pivot_df.reindex(columns=all_hours)
    
    # Rename columns: 0 -> "Hr 1", 1 -> "Hr 2", etc.
    pivot_df.columns = [f"Hr {i+1}" for i in all_hours]
    
    # 5. Reset index to make date a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Format the date column
    # Target format: MM/DD/YYYY
    pivot_df['Date'] = pivot_df['date_only'].apply(lambda x: x.strftime('%m/%d/%Y') if pd.notnull(x) else None)
    
    # 7. Select and order columns
    # Target columns: Date, Hr 1, ..., Hr 24
    cols = ['Date'] + [f"Hr {i}" for i in range(1, 25)]
    result = pivot_df[cols]
    
    # 8. Sort by Date descending (as per target sample)
    # Convert Date back to datetime for sorting, then drop helper if needed, 
    # but since we formatted as string, we can sort by the original date_only or parse again.
    # Easier: sort by the 'date_only' column before dropping it, or parse 'Date' string.
    # Let's sort by the original date_only which is still in the dataframe if we didn't drop it.
    # Actually, we reset index, so 'date_only' is a column.
    result = result.sort_values(by='date_only', ascending=False)
    
    # Drop the helper column 'date_only'
    result = result.drop(columns=['date_only'])
    
    return result
