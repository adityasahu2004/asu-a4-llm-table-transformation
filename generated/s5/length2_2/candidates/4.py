import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format dt_strata: Sample shows "1/1/2011", "1/17/2011", "2/3/2011". 
    # This implies no leading zeros for month/day if they are single digits.
    # Standard strftime %m/%d/%Y gives 01/01/2011.
    # We can strip leading zeros from month and day parts.
    dt_strata = dates.dt.strftime('%m/%d/%Y').apply(lambda x: '/'.join([str(int(p)) for p in x.split('/')]))
    
    # Calculate dow: ISO weekday (Mon=1, Sun=7)
    dow = dates.dt.dayofweek + 1
    
    # Map value1..value24 to pct_hourly_0100..pct_hourly_2400
    hourly_cols = {}
    for i in range(1, 25):
        src_col = f'value{i}'
        tgt_col = f'pct_hourly_{i:02d}00'
        hourly_cols[tgt_col] = source[src_col]
        
    # Construct the result dataframe
    out = pd.DataFrame(hourly_cols, index=source.index)
    out['dt_strata'] = dt_strata
    out['dow'] = dow
    out['pct_hourly_2500'] = 0
    
    # Reorder columns to match target schema
    cols = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 26)]
    out = out[cols]
    
    return out.reset_index(drop=True)
