import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date string from DT_STRATA (e.g., "7/2/2016")
    dt_parsed = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    
    # Format to MM/DD/YYYY for the 'date' column
    date_col = dt_parsed.dt.strftime('%m/%d/%Y')
    
    # Build the result DataFrame
    result = pd.DataFrame()
    result['date'] = date_col
    
    # Map PCT_HOURLY_XX00 to Hour XX
    for h in range(1, 25):
        src_col = f'PCT_HOURLY_{h:02d}00'
        tgt_col = f'Hour {h}'
        result[tgt_col] = source[src_col]
        
    return result
