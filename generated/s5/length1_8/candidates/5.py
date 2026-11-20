import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format in source: "7/28/2019 4:50" -> %m/%d/%Y %H:%M
    # Note: Single digit months/days/hours are possible.
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date for grouping and hour for pivoting
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Map hour 0 to 24, others remain same
    df['hour_label'] = df['hour'].replace(0, 24)
    
    # Pivot the data
    # Index: date_only, Columns: hour_label, Values: cerc_logger_1
    pivoted = df.pivot_table(index='date_only', columns='hour_label', values='cerc_logger_1')
    
    # Rename columns to match target format "H:00"
    pivoted.columns = [f"{int(col)}:00" for col in pivoted.columns]
    
    # Create the 'cst' column from the index
    # Format: "Sat 07/20/2019" -> %a %m/%d/%Y
    pivoted.index = pd.to_datetime(pivoted.index).strftime('%a %m/%d/%Y')
    pivoted.index.name = 'cst'
    
    # Reset index to make 'cst' a column
    result = pivoted.reset_index()
    
    # Sort by date descending to match the sample order observed (2019 -> 2018)
    # We need to parse the cst string back to datetime to sort correctly, or use the original date_only
    # Since we lost the original date_only in the pivot index name, let's re-parse or just sort by the string if format allows?
    # String sort on "Sat 07/20/2019" is not chronological.
    # Let's add a temporary sort key.
    
    # Re-create a datetime column for sorting
    result['sort_key'] = pd.to_datetime(result['cst'], format='%a %m/%d/%Y')
    result = result.sort_values('sort_key', ascending=False)
    result = result.drop(columns=['sort_key'])
    
    # Ensure column order matches target exactly
    # Target: cst, 1:00, 2:00, ..., 24:00
    cols = ['cst'] + [f"{h}:00" for h in range(1, 25)]
    result = result[cols]
    
    return result.reset_index(drop=True)
