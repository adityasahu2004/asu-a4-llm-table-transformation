import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame by:
    1. Selecting the date and 24 hourly columns.
    2. Renaming hourly columns to value1-value24 in chronological order.
    3. Parsing and formatting the date column.
    """
    
    # Define the mapping from source hour columns to target value columns
    # Chronological order: 12 AM, 1 AM, ..., 11 AM, 12 PM, 1 PM, ..., 11 PM
    hour_mapping = {
        "12:00 AM": "value1",
        "1:00 AM": "value2",
        "2:00 AM": "value3",
        "3:00 AM": "value4",
        "4:00 AM": "value5",
        "5:00 AM": "value6",
        "6:00 AM": "value7",
        "7:00 AM": "value8",
        "8:00 AM": "value9",
        "9:00 AM": "value10",
        "10:00 AM": "value11",
        "11:00 AM": "value12",
        "12:00 PM": "value13",
        "1:00 PM": "value14",
        "2:00 PM": "value15",
        "3:00 PM": "value16",
        "4:00 PM": "value17",
        "5:00 PM": "value18",
        "6:00 PM": "value19",
        "7:00 PM": "value20",
        "8:00 PM": "value21",
        "9:00 PM": "value22",
        "10:00 PM": "value23",
        "11:00 PM": "value24"
    }
    
    # Identify source columns to keep
    source_hour_cols = list(hour_mapping.keys())
    cols_to_keep = ["date"] + source_hour_cols
    
    # Filter the source dataframe to only include relevant columns
    # This handles cases where extra columns like 'DSL' exist
    df_filtered = source[cols_to_keep].copy()
    
    # Rename the hourly columns
    df_filtered.rename(columns=hour_mapping, inplace=True)
    
    # Parse the date column
    # Source format is M/D/YYYY (e.g., "7/3/2014")
    # Target format is YYYY-MM-DD HH:MM:SS (e.g., "2014-01-01 00:00:00")
    df_filtered["date"] = pd.to_datetime(df_filtered["date"], format="%m/%d/%Y")
    df_filtered["date"] = df_filtered["date"].dt.strftime("%Y-%m-%d %H:%M:%S")
    
    # Ensure column order matches target specification
    target_cols = ["date"] + [f"value{i}" for i in range(1, 25)]
    result = df_filtered[target_cols]
    
    return result
