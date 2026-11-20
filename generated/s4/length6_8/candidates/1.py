import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date string
    # Format observed: "7/28/2019 4:50" -> %m/%d/%Y %H:%M
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %I:%M %p', errors='coerce')
    
    # If parsing with 12-hour fails due to ambiguity or format variations, try generic or specific 24h if needed.
    # The sample shows "4:50", "9:30", "18:50". 18:50 implies 24-hour format in the string potentially, 
    # or just mixed. Let's look closer: "18:50" is definitely 24h. "4:50" is ambiguous but likely AM.
    # However, standard pd.to_datetime handles "7/28/2019 4:50" correctly. 
    # It also handles "18:50" correctly if we don't enforce %I.
    # Let's use a robust parser or just infer.
    # Re-evaluating: "7/28/2019 4:50" and "11/2/2019 18:50". 
    # pd.to_datetime usually infers this well.
    
    # Extract date part for grouping
    df['date_key'] = df['dt'].dt.date
    
    # Extract hour part. 
    # We need to map 0-23 to 1-24 for the target column names.
    # Hour 0 -> Hr 24
    # Hour 1 -> Hr 1
    # ...
    # Hour 23 -> Hr 23
    df['hour_int'] = df['dt'].dt.hour
    df['hour_label'] = df['hour_int'].apply(lambda h: 24 if h == 0 else h)

    # Pivot the data
    # Index: date_key
    # Columns: hour_label
    # Values: cerc_logger_1
    # Since source rows are unique timestamps, we can just use 'first' or 'mean' (same result)
    # But strictly, if there are multiple entries for same hour/day, we might need aggregation.
    # The problem statement implies a deterministic transformation. 
    # Given distinct rows = source rows, it's likely 1 value per hour per day.
    
    pivoted = df.pivot_table(index='date_key', columns='hour_label', values='cerc_logger_1', aggfunc='first')
    
    # Rename columns to match target format "Hr X"
    pivoted.columns = [f'Hr {col}' for col in pivoted.columns]
    
    # Sort columns to ensure order Hr 1, Hr 2, ... Hr 24
    # The pivot might not preserve numeric order if labels are strings.
    # We can sort by the integer part of the column name.
    pivoted = pivoted.reindex(sorted(pivoted.columns, key=lambda x: int(x.split(' ')[1])), axis=1)
    
    # Format the index as Date string MM/DD/YYYY
    pivoted.index = pd.to_datetime(pivoted.index).strftime('%m/%d/%Y')
    pivoted.index.name = 'Date'
    
    # Reset index to make Date a column
    result = pivoted.reset_index()
    
    return result
