import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    dt = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    # Build output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Format date
    out['dt_strata'] = dt.dt.strftime('%m/%d/%Y')
    
    # Day of week (ISO: Mon=1, Sun=7)
    out['dow'] = dt.dt.dayofweek + 1
    
    # Map hourly columns
    # Source cols: '1:00' ... '23:00', '24:00:00'
    # Target cols: 'pct_hourly_0100' ... 'pct_hourly_2400'
    for h in range(1, 25):
        src_col = f'{h}:00' if h < 24 else '24:00:00'
        tgt_col = f'pct_hourly_{h:02d}00'
        out[tgt_col] = source[src_col]
        
    # Add constant 25th hour
    out['pct_hourly_2500'] = 0
    
    # Ensure correct column order
    cols = ['dt_strata', 'dow'] + [f'pct_hourly_{h:02d}00' for h in range(1, 26)]
    return out[cols].reset_index(drop=True)
