import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column from source format 'M/D/YYYY'
    dates = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    
    # Format to target string 'MM/DD/YYYY'
    date_str = dates.dt.strftime('%m/%d/%Y')
    
    # Map source hourly columns to target hourly columns
    hourly_cols = [f'PCT_HOURLY_{h:02d}00' for h in range(1, 25)]
    target_hourly_cols = [f'Hour {h}' for h in range(1, 25)]
    
    # Create the result dataframe
    result = pd.DataFrame()
    result['date'] = date_str
    
    for src_col, tgt_col in zip(hourly_cols, target_hourly_cols):
        result[tgt_col] = source[src_col]
        
    return result
