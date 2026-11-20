import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Identify hourly columns to include (exclude 2500 as it's not in target)
    hourly_cols = [col for col in source.columns if col.startswith('PCT_HOURLY_') and col != 'PCT_HOURLY_2500']
    
    # Parse the date column
    # Source format is M/D/YYYY, e.g., "7/2/2016"
    df = source.copy()
    df['DT_STRATA'] = pd.to_datetime(df['DT_STRATA'], format='%m/%d/%Y')
    
    # Group by date and calculate the mean of the hourly percentages
    # We select only the necessary columns for aggregation to avoid issues with other string columns
    agg_cols = hourly_cols
    grouped = df.groupby('DT_STRATA')[agg_cols].mean()
    
    # Rename columns from PCT_HOURLY_HH00 to HH:00
    new_col_names = {}
    for col in grouped.columns:
        # Extract the hour part, e.g., PCT_HOURLY_0100 -> 0100
        hour_part = col.split('_')[-1]
        # Convert to integer to remove leading zeros, then format as HH:00
        # Note: 0100 -> 1, 1200 -> 12, 2400 -> 24
        hour_int = int(hour_part)
        new_col_names[col] = f"{hour_int}:00"
        
    grouped.rename(columns=new_col_names, inplace=True)
    
    # Format the date index into the target string format: "Fri 01/01/2016"
    # Format: %a %m/%d/%Y
    cst_strings = grouped.index.strftime('%a %m/%d/%Y')
    
    # Create the final DataFrame
    result = grouped.reset_index(drop=True)
    result.insert(0, 'cst', cst_strings)
    
    # Ensure column order matches target: cst, 1:00, 2:00, ..., 24:00
    # The hourly columns should already be in order if the source was ordered, 
    # but let's enforce it to be safe.
    target_hour_cols = [f"{h}:00" for h in range(1, 25)]
    result = result[['cst'] + target_hour_cols]
    
    return result
