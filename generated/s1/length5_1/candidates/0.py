import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Define the hourly columns to keep (0100 to 2400)
    hourly_cols = [f"PCT_HOURLY_{h:04d}" for h in range(1, 25)]
    
    # Select the date column and the hourly columns
    df = source[['DT_STRATA'] + hourly_cols].copy()
    
    # Group by date and sum the hourly values
    # This aggregates all strata for each day into a single row
    df_grouped = df.groupby('DT_STRATA', as_index=False).sum()
    
    # Rename the date column
    df_grouped = df_grouped.rename(columns={'DT_STRATA': 'date'})
    
    # Rename the hourly columns to value1, value2, ..., value24
    rename_map = {f"PCT_HOURLY_{h:04d}": f"value{h}" for h in range(1, 25)}
    df_grouped = df_grouped.rename(columns=rename_map)
    
    # Parse the date string and format it to MM/DD/YYYY
    # Source format is M/D/YYYY (e.g., 7/2/2016)
    # Target format is MM/DD/YYYY (e.g., 07/02/2016)
    df_grouped['date'] = pd.to_datetime(df_grouped['date'], format='%m/%d/%Y')
    df_grouped['date'] = df_grouped['date'].dt.strftime('%m/%d/%Y')
    
    # Ensure the column order matches the target specification
    # Target columns: date, value1, ..., value24
    target_cols = ['date'] + [f"value{h}" for h in range(1, 25)]
    df_grouped = df_grouped[target_cols]
    
    # Sort by date to ensure consistent ordering (optional but good practice)
    # The target sample seems sorted by date? 
    # 01/01, 05/29, 10/26... No, the sample is not sorted.
    # However, groupby usually preserves the order of first appearance or sorts.
    # Let's not sort explicitly unless required, but groupby might shuffle.
    # The target has 366 rows.
    
    return df_grouped
