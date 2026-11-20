import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame by filtering for standard weekdays,
    formatting the date, and renaming hourly percentage columns.
    """
    # 1. Filter for standard weekdays (1-7). Exclude 'H' (Holiday) and 'D' (Other/DS).
    valid_dows = ['1', '2', '3', '4', '5', '6', '7']
    df = source[source['DOW'].isin(valid_dows)].copy()
    
    # 2. Parse and format the date
    # Source format is M/D/YYYY (e.g., "7/2/2016")
    # Target format is MM/DD/YYYY (e.g., "07/02/2016")
    df['date'] = pd.to_datetime(df['DT_STRATA'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 3. Rename hourly columns
    # Source: PCT_HOURLY_0100 ... PCT_HOURLY_2400
    # Target: Hour 1 ... Hour 24
    
    rename_map = {}
    for i in range(1, 25):
        src_col = f"PCT_HOURLY_{i:04d}"
        tgt_col = f"Hour {i}"
        if src_col in df.columns:
            rename_map[src_col] = tgt_col
            
    df.rename(columns=rename_map, inplace=True)
    
    # 4. Select and order columns
    # Target columns: date, Hour 1, ..., Hour 24
    target_cols = ['date'] + [f"Hour {i}" for i in range(1, 25)]
    
    # Ensure we only select columns that exist (though logic above guarantees it for 1-24)
    final_cols = [col for col in target_cols if col in df.columns]
    
    result = df[final_cols]
    
    return result
