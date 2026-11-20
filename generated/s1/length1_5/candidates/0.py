import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'])
    
    # 2. Sort by date to ensure chronological order
    df = df.sort_values('date').reset_index(drop=True)
    
    # 3. Create the 'cst' column with the specified format
    # Format: "Thu 01/01/2015" -> %a %m/%d/%Y
    df['cst'] = df['date'].dt.strftime('%a %m/%d/%Y')
    
    # 4. Rename Hour columns to HH:00 format
    rename_map = {}
    for i in range(1, 25):
        old_name = f"Hour {i}"
        new_name = f"{i}:00"
        if old_name in df.columns:
            rename_map[old_name] = new_name
            
    df = df.rename(columns=rename_map)
    
    # 5. Drop the original date column
    df = df.drop(columns=['date'])
    
    # 6. Reorder columns: 'cst' first, then the hour columns in order
    hour_cols = [f"{i}:00" for i in range(1, 25)]
    final_cols = ['cst'] + hour_cols
    
    # Ensure we only select columns that exist
    existing_cols = [c for c in final_cols if c in df.columns]
    df = df[existing_cols]
    
    return df
