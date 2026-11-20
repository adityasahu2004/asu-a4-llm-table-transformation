import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format as MM/DD/YYYY
    dt = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    date_col = dt.dt.strftime('%m/%d/%Y')
    
    # Select and rename hourly columns
    hour_cols = [f'PCT_HOURLY_{h:02d}00' for h in range(1, 25)]
    new_hour_cols = [f'Hour {h}' for h in range(1, 25)]
    
    # Build the result DataFrame
    result = pd.DataFrame({
        'date': date_col
    }, index=source.index)
    
    for src_col, dst_col in zip(hour_cols, new_hour_cols):
        result[dst_col] = source[src_col]
        
    return result.reset_index(drop=True)
