import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the Date column
    # The source date format is M/D/YYYY
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Create dt_strata
    # Format as M/D/YYYY (no leading zeros)
    df['dt_strata'] = df['parsed_date'].dt.strftime('%-m/%-d/%Y')
    
    # 3. Create dow
    # Mapping: Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6, Sun=0
    # Python weekday(): Mon=0, ..., Sun=6
    # Formula: (weekday() + 1) % 7
    df['dow'] = (df['parsed_date'].dt.weekday + 1) % 7
    
    # 4. Rename hourly columns
    # Source columns '1' through '24' become 'pct_hourly_0100' through 'pct_hourly_2400'
    rename_map = {}
    for i in range(1, 25):
        rename_map[str(i)] = f'pct_hourly_{i:04d}'
    
    df = df.rename(columns=rename_map)
    
    # 5. Add pct_hourly_2500 column with NaN
    df['pct_hourly_2500'] = np.nan
    
    # 6. Select and order columns
    # Target order: dt_strata, dow, pct_hourly_0100 ... pct_hourly_2500
    hourly_cols = [f'pct_hourly_{i:04d}' for i in range(1, 26)]
    final_cols = ['dt_strata', 'dow'] + hourly_cols
    
    result = df[final_cols]
    
    # 7. Sort by dt_strata to match typical target presentation (optional but good practice)
    # The target sample is sorted by date.
    result = result.sort_values('dt_strata').reset_index(drop=True)
    
    return result
