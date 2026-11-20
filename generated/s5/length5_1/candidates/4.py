import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format as MM/DD/YYYY
    dates = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    date_strs = dates.dt.strftime('%m/%d/%Y')
    
    # Map hourly columns to new names
    col_map = {}
    for h in range(1, 25):
        src_col = f'PCT_HOURLY_{h:02d}00'
        tgt_col = f'value{h}'
        col_map[src_col] = tgt_col
        
    # Select and rename the hourly columns
    hour_cols = [f'PCT_HOURLY_{h:02d}00' for h in range(1, 25)]
    df_hours = source[hour_cols].rename(columns=col_map)
    
    # Construct final dataframe
    result = pd.DataFrame({'date': date_strs})
    result = pd.concat([result, df_hours], axis=1)
    
    return result.reset_index(drop=True)
