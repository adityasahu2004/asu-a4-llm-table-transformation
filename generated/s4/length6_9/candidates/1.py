import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['parsed_dt'] = pd.to_datetime(df['date'])
    
    # Extract calendar date for grouping
    df['cal_date'] = df['parsed_dt'].dt.date
    
    # Sort by calendar date and parsed datetime to ensure correct ordering
    df = df.sort_values(['cal_date', 'parsed_dt'])
    
    # Assign a rank within each date group (1-based)
    # This assumes roughly 24 records per day, mapping to Hr 1 - Hr 24
    df['hr_rank'] = df.groupby('cal_date').cumcount() + 1
    
    # Filter to only include ranks 1-24 if necessary, or let pivot handle it
    # The target has columns Hr 1 to Hr 24.
    
    # Create the pivot table
    # Values: zone_016
    # Index: cal_date
    # Columns: hr_rank
    pivot_df = df.pivot_table(index='cal_date', columns='hr_rank', values='zone_016', aggfunc='first')
    
    # Rename columns to "Hr 1", "Hr 2", etc.
    pivot_df.columns = [f'Hr {int(c)}' for c in pivot_df.columns]
    
    # Ensure we have columns 1-24, filling missing with NaN
    expected_cols = [f'Hr {i}' for i in range(1, 25)]
    for col in expected_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # Select only the expected columns
    pivot_df = pivot_df[expected_cols]
    
    # Reset index to make Date a column
    pivot_df = pivot_df.reset_index()
    
    # Format the Date column as MM/DD/YYYY
    pivot_df['Date'] = pd.to_datetime(pivot_df['cal_date']).dt.strftime('%m/%d/%Y')
    
    # Drop the temporary cal_date column if it wasn't dropped by reset_index behavior (it is the index now)
    # reset_index makes 'cal_date' a column. We want 'Date' as the name.
    # We already created 'Date'. We can drop 'cal_date'.
    pivot_df = pivot_df.drop(columns=['cal_date'])
    
    # Reorder columns: Date first, then Hr 1-24
    final_cols = ['Date'] + expected_cols
    pivot_df = pivot_df[final_cols]
    
    return pivot_df
