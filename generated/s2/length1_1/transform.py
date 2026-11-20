import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date string
    dt = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    
    # Format cst as "DayOfWeek MM/DD/YYYY"
    # %a gives abbreviated weekday name (e.g., Fri)
    cst_str = dt.dt.strftime('%a %m/%d/%Y')
    
    # Build the output dataframe
    out = pd.DataFrame()
    out['cst'] = cst_str
    
    # Map PCT_HOURLY_XX00 to H:00
    for h in range(1, 25):
        src_col = f'PCT_HOURLY_{h:02d}00'
        tgt_col = f'{h}:00'
        out[tgt_col] = source[src_col]
        
    return out
