import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    
    # Create the output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Extract month name and pad to 10 characters
    month_names = dates.dt.strftime('%B')
    out['month'] = month_names.str.pad(10, side='right')
    
    # Set daytype to weekday
    out['daytype'] = 'weekday'
    
    # Rename and select hourly columns
    for h in range(1, 25):
        src_col = f'PCT_HOURLY_{h:02d}00'
        tgt_col = f'hr{h}'
        out[tgt_col] = source[src_col]
        
    return out.reset_index(drop=True)
