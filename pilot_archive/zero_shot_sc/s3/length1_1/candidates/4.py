import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame by:
    1. Parsing the DT_STRATA date column.
    2. Formatting it into the 'cst' column as "Dow MM/DD/YYYY".
    3. Renaming the PCT_HOURLY columns to "H:00" format.
    4. Dropping unused columns.
    """
    
    # Create a copy to avoid modifying the original source
    df = source.copy()
    
    # 1. Parse DT_STRATA to datetime
    # The format observed is MM/DD/YYYY
    df['parsed_date'] = pd.to_datetime(df['DT_STRATA'], format='%m/%d/%Y')
    
    # 2. Format the date into the target 'cst' string format
    # Target sample shows: "Fri 01/01/2016" -> "%a %m/%d/%Y"
    df['cst'] = df['parsed_date'].dt.strftime('%a %m/%d/%Y')
    
    # 3. Define the mapping for hourly columns
    # Source: PCT_HOURLY_0100 ... PCT_HOURLY_2400
    # Target: 1:00 ... 24:00
    
    rename_map = {}
    for hour in range(1, 25):
        source_col = f"PCT_HOURLY_{hour:04d}"
        target_col = f"{hour}:00"
        rename_map[source_col] = target_col
        
    # Rename the columns
    df.rename(columns=rename_map, inplace=True)
    
    # 4. Select the required columns in the correct order
    # Target columns: cst, 1:00, 2:00, ..., 24:00
    
    target_cols = ['cst']
    for hour in range(1, 25):
        target_cols.append(f"{hour}:00")
        
    result = df[target_cols]
    
    # Ensure dtypes are correct (float64 for hourly columns)
    for col in target_cols[1:]:
        result[col] = result[col].astype('float64')
        
    return result
