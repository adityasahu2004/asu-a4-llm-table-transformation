import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date string
    dates = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    
    # Create the output DataFrame
    out = pd.DataFrame(index=source.index)
    
    # Format month: Full name, right-padded to 10 chars
    # %B gives full month name. We manually pad to match the distinct values in target.
    month_names = dates.dt.strftime('%B')
    out['month'] = month_names.str.pad(width=10, side='right')
    
    # Set daytype to constant
    out['daytype'] = 'weekday'
    
    # Map PCT_HOURLY_XX00 to hrXX
    for h in range(1, 25):
        src_col = f'PCT_HOURLY_{h:02d}00'
        tgt_col = f'hr{h}'
        out[tgt_col] = source[src_col]
        
    return out.reset_index(drop=True)
