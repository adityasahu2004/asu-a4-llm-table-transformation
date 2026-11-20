import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    dt = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    
    # Create month column with specific padding
    # Target distinct values show month names padded to 10 chars
    month_names = dt.dt.strftime('%B')
    month_padded = month_names.str.pad(10, side='right')
    
    # Create daytype column
    daytype = pd.Series(['weekday'] * len(source), index=source.index)
    
    # Select and rename hourly columns
    hourly_cols = [f'PCT_HOURLY_{h:02d}00' for h in range(1, 25)]
    new_hourly_cols = [f'hr{h}' for h in range(1, 25)]
    
    out = pd.DataFrame(index=source.index)
    out['month'] = month_padded
    out['daytype'] = daytype
    
    for src_col, tgt_col in zip(hourly_cols, new_hourly_cols):
        out[tgt_col] = source[src_col]
        
    return out.reset_index(drop=True)
