import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    # The source date format is M/D/YYYY (e.g., "7/3/2015")
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Create dt_strata column formatted as M/D/YYYY
    # Using strftime to match the target string format exactly
    df['dt_strata'] = df['parsed_date'].dt.strftime('%m/%d/%Y')
    
    # 3. Create dow column (0=Monday, ..., 6=Sunday)
    df['dow'] = df['parsed_date'].dt.dayofweek.astype('int64')
    
    # 4. Rename Hour columns to pct_hourly_XX00
    rename_map = {}
    for i in range(1, 25):
        old_col = f'Hour {i}'
        new_col = f'pct_hourly_{i:02d}00'
        rename_map[old_col] = new_col
    
    df = df.rename(columns=rename_map)
    
    # 5. Add the new column pct_hourly_2500 with NaN
    df['pct_hourly_2500'] = np.nan
    
    # 6. Select and order columns
    # Target order: dt_strata, dow, pct_hourly_0100 ... pct_hourly_2500
    hourly_cols = [f'pct_hourly_{i:02d}00' for i in range(1, 26)]
    final_cols = ['dt_strata', 'dow'] + hourly_cols
    
    df = df[final_cols]
    
    # 7. Sort by dt_strata to match target sample order (chronological)
    # Since dt_strata is string M/D/YYYY, sorting lexicographically works for same-year dates.
    # To be safe, sort by the parsed date then drop it.
    df = df.sort_values(by='parsed_date').reset_index(drop=True)
    
    # Drop the helper column
    df = df.drop(columns=['parsed_date'])
    
    return df
