import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Drop the 'Class' column as it is not in the target
    if 'Class' in df.columns:
        df = df.drop(columns=['Class'])
    
    # 2. Rename the 'Date' column to 'cst'
    df = df.rename(columns={'Date': 'cst'})
    
    # 3. Rename numeric columns 1-24 to '1:00'-'24:00'
    rename_map = {}
    for col in df.columns:
        if col != 'cst':
            # Check if column is a number (int or float) representing 1-24
            try:
                col_int = int(col)
                if 1 <= col_int <= 24:
                    rename_map[col] = f"{col_int}:00"
            except (ValueError, TypeError):
                pass
    
    df = df.rename(columns=rename_map)
    
    # 4. Format the 'cst' column
    # Parse dates assuming format M/D/YYYY
    df['cst'] = pd.to_datetime(df['cst'], format='%m/%d/%Y')
    # Format to 'Tue 01/01/2013' -> %a %m/%d/%Y
    df['cst'] = df['cst'].dt.strftime('%a %m/%d/%Y')
    
    # 5. Ensure column order: 'cst' first, then 1:00 to 24:00
    # Construct the expected column list
    expected_cols = ['cst'] + [f"{i}:00" for i in range(1, 25)]
    
    # Filter to only include columns that exist in the dataframe (in case some hours are missing)
    final_cols = [col for col in expected_cols if col in df.columns]
    
    # Reorder columns
    df = df[final_cols]
    
    # Reset index to ensure clean integer index
    df = df.reset_index(drop=True)
    
    return df
