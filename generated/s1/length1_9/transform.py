import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    # Format in source: "M/D/YYYY H:MM"
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract hour and map to target column names
    # Target columns are "1:00" to "24:00"
    # Mapping: Hour 0 -> "1:00", Hour 1 -> "2:00", ..., Hour 23 -> "24:00"
    df['hour'] = df['date'].dt.hour
    df['target_col'] = df['hour'].apply(lambda h: f"{h+1}:00")
    
    # 3. Prepare for pivot
    # We need to group by the date (as string in target format) and pivot on target_col
    # First, create the date string in the target format: "Day MM/DD/YYYY"
    df['cst'] = df['date'].dt.strftime('%a %m/%d/%Y')
    
    # 4. Pivot the data
    # We use 'cst' as index, 'target_col' as columns, and 'zone_016' as values
    # Since there might be multiple entries or missing entries, we aggregate.
    # The target has 0 nulls, implying missing values are 0.0.
    # We use 'max' or 'sum' or 'first'. Given the nature of such data, 
    # if there's only one reading per hour, 'first' or 'max' works. 
    # If there are multiple, 'sum' might be intended if they are partial, 
    # but 'max' is safer for "latest status". However, looking at the distinct values 
    # in the target, they are specific floats. Let's assume one value per bin.
    # We will use 'max' to handle potential duplicates gracefully, then fillna.
    
    pivot_df = df.pivot_table(
        index='cst', 
        columns='target_col', 
        values='zone_016', 
        aggfunc='max' # or 'first', 'max' is robust for single values
    )
    
    # 5. Ensure all 24 columns exist and fill missing with 0.0
    expected_cols = [f"{h}:00" for h in range(1, 25)]
    
    # Reindex columns to ensure all expected columns are present
    pivot_df = pivot_df.reindex(columns=expected_cols, fill_value=0.0)
    
    # 6. Reset index to make 'cst' a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Ensure column order matches target exactly
    # Target order: cst, 1:00, 2:00, ..., 24:00
    final_cols = ['cst'] + expected_cols
    result = pivot_df[final_cols]
    
    # 8. Ensure dtypes are float64 for numeric columns
    for col in expected_cols:
        result[col] = result[col].astype('float64')
        
    return result
