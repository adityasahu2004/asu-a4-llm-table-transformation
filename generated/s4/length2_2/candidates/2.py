import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column. Format M/D/YYYY handles single/double digit months/days.
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Construct the output DataFrame
    out = pd.DataFrame(index=source.index)
    
    # Format date string as M/D/YYYY (non-zero-padded)
    # Using strftime with %m/%d/%Y usually zero-pads, but the sample shows "1/1/2011".
    # However, pandas strftime %m/%d/%Y on 1/1/2011 produces "01/01/2011".
    # Let's look closely at the target sample: "1/1/2011", "1/17/2011", "2/3/2011".
    # This implies non-zero-padded. Pandas strftime doesn't support non-zero-padded easily without manual strip.
    # But wait, standard strftime %m/%d/%Y gives 01/01/2011.
    # Let's check if the target really wants non-zero padded.
    # Sample: "1/1/2011", "1/17/2011", "2/3/2011", "2/19/2011", "3/8/2011", "3/24/2011", "4/10/2011", "4/26/2011", "5/13/2011", "5/29/2011", "6/15/2011", "7/2/2011".
    # Yes, it is non-zero padded.
    # We can achieve this by formatting and stripping leading zeros, or using a custom formatter.
    # A robust way: dt.strftime('%m/%d/%Y').str.lstrip('0') -> this might break if day is 10 (becomes /10).
    # Better: dt.apply(lambda x: f"{x.month}/{x.day}/{x.year}")
    out['dt_strata'] = dt.apply(lambda x: f"{x.month}/{x.day}/{x.year}")
    
    # Day of week: Monday=1 ... Sunday=7
    out['dow'] = dt.dt.dayofweek + 1
    
    # Map value1..value24 to pct_hourly_0100..pct_hourly_2400
    for h in range(1, 25):
        out[f'pct_hourly_{h:02d}00'] = source[f'value{h}']
        
    # Add the constant 25th hour
    out['pct_hourly_2500'] = 0
    
    return out.reset_index(drop=True)
