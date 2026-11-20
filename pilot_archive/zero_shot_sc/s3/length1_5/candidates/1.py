import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column to datetime for sorting and formatting
    df = source.copy()
    df['date_parsed'] = pd.to_datetime(df['date'])
    
    # 2. Sort by date to ensure chronological order
    df = df.sort_values('date_parsed').reset_index(drop=True)
    
    # 3. Create the 'cst' column with the specific format "Ddd MM/DD/YYYY"
    # %a gives abbreviated weekday name (e.g., Thu)
    df['cst'] = df['date_parsed'].dt.strftime('%a %m/%d/%Y')
    
    # 4. Rename columns from "Hour N" to "N:00"
    rename_map = {}
    for i in range(1, 25):
        rename_map[f'Hour {i}'] = f'{i}:00'
    df = df.rename(columns=rename_map)
    
    # 5. Drop the helper and original date columns
    df = df.drop(columns=['date', 'date_parsed'])
    
    # 6. Ensure correct dtypes
    # Columns 9:00 to 16:00 should be int64, others float64
    int_cols = [f'{i}:00' for i in range(9, 17)]
    float_cols = [f'{i}:00' for i in range(1, 25) if i not in range(9, 17)]
    
    for col in int_cols:
        if col in df.columns:
            # Fill NaNs with 0 if necessary for int conversion, though source has 0 nulls
            df[col] = df[col].fillna(0).astype('int64')
            
    for col in float_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('float64')
            
    # 7. Reorder columns to match target schema: cst first, then hours 1:00 to 24:00
    col_order = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    df = df[col_order]
    
    return df
