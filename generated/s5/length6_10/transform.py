import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the source date column
    # The source format is ambiguous but samples show "11/6/2018 21:45".
    # pd.to_datetime handles this mixed format well.
    df = source.copy()
    df['parsed_dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract Day and Hour
    df['day'] = df['parsed_dt'].dt.date
    df['hour'] = df['parsed_dt'].dt.hour
    
    # 3. Map Hour (0-23) to Target Column Names ("Hr 24", "Hr 1", ... "Hr 23")
    # Hour 0 -> Hr 24
    # Hour 1 -> Hr 1
    # ...
    # Hour 23 -> Hr 23
    def map_hour_to_col(h):
        if h == 0:
            return 'Hr 24'
        else:
            return f'Hr {h}'
            
    df['col_name'] = df['hour'].apply(map_hour_to_col)
    
    # 4. Pivot the data
    # We group by day and col_name, taking the first value of zone_016_cooling_sp
    # This handles potential duplicates and creates the wide format
    pivot_df = df.groupby(['day', 'col_name'])['zone_016_cooling_sp'].first().unstack(fill_value=np.nan)
    
    # 5. Reset index to make 'day' a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Format the Date column
    pivot_df['Date'] = pd.to_datetime(pivot_df['day']).dt.strftime('%m/%d/%Y')
    
    # 7. Select and order columns to match target exactly
    # Target columns: Date, Hr 1, Hr 2, ... Hr 24
    target_cols = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # Ensure all hour columns exist (even if empty/NaN)
    for col in target_cols[1:]:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    result = pivot_df[target_cols]
    
    return result.reset_index(drop=True)
