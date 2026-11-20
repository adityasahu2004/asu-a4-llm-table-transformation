import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame by:
    1. Extracting the month name from DT_STRATA and formatting it to 11 chars.
    2. Setting daytype to 'weekday' for all rows.
    3. Renaming PCT_HOURLY_XX00 columns to hrX.
    4. Dropping unused columns.
    """
    
    # 1. Parse Date and Extract Month
    # Format is M/D/YYYY
    dt = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    
    # Extract month name
    month_names = dt.dt.strftime('%B')
    
    # Format to match target: Left aligned, padded to 11 characters
    # e.g., "January" -> "January  " (2 spaces)
    # "September" -> "September" (0 spaces)
    # "December" -> "December " (1 space)
    month_formatted = month_names.str.ljust(11)
    
    # 2. Determine Day Type
    # Target schema shows only "weekday" as distinct value.
    # Sample data shows Sundays (7) mapped to "weekday".
    # Therefore, map all rows to "weekday".
    daytype = pd.Series(['weekday'] * len(source), index=source.index)
    
    # 3. Rename Hourly Columns
    # Map PCT_HOURLY_0100 -> hr1, ..., PCT_HOURLY_2400 -> hr24
    rename_map = {}
    for i in range(1, 25):
        src_col = f"PCT_HOURLY_{i:04d}"
        tgt_col = f"hr{i}"
        if src_col in source.columns:
            rename_map[src_col] = tgt_col
            
    # Select and rename columns
    # We need to keep the order: month, daytype, hr1...hr24
    df_out = pd.DataFrame()
    df_out['month'] = month_formatted
    df_out['daytype'] = daytype
    
    # Add hourly columns in order
    for i in range(1, 25):
        src_col = f"PCT_HOURLY_{i:04d}"
        tgt_col = f"hr{i}"
        if src_col in source.columns:
            df_out[tgt_col] = source[src_col].astype(float)
            
    return df_out
