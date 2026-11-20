import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame by:
    1. Formatting the DT_STRATA column into MM/DD/YYYY format and renaming to 'Date'.
    2. Renaming PCT_HOURLY_XX00 columns to 'Hr X'.
    3. Dropping unused columns (Strata_ID, Strata, DOW, PCT_HOURLY_2500).
    """
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Format Date
    # Parse the date string and format it to MM/DD/YYYY
    # Source format is M/D/YYYY, Target is MM/DD/YYYY
    df['Date'] = pd.to_datetime(df['DT_STRATA'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 2. Define mapping for hourly columns
    # Source: PCT_HOURLY_0100 ... PCT_HOURLY_2400
    # Target: Hr 1 ... Hr 24
    
    rename_map = {}
    for i in range(1, 25):
        src_col = f"PCT_HOURLY_{i:04d}"
        tgt_col = f"Hr {i}"
        rename_map[src_col] = tgt_col
        
    # 3. Select and rename columns
    # We only want the Date column and the 24 hourly columns
    cols_to_keep = ['Date'] + [f"Hr {i}" for i in range(1, 25)]
    
    # Rename the relevant columns in the dataframe
    df_renamed = df.rename(columns=rename_map)
    
    # Select only the required columns
    result = df_renamed[cols_to_keep]
    
    return result
