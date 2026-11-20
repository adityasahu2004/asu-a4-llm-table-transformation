import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create the output DataFrame
    out = pd.DataFrame(index=source.index)
    
    # Format dt_strata as M/D/YYYY (e.g., 1/1/2014)
    # Using mixed format to allow single digit months/days if present, though standard %m/%d/%Y pads.
    # The sample shows '1/1/2014', '7/2/2014'. pd strftime '%m/%d/%Y' produces '01/01/2014'.
    # We need to strip leading zeros if they exist to match the sample exactly.
    # However, the target schema says distinct values are dates. 
    # Let's check the sample carefully: "1/1/2014", "7/2/2014".
    # Standard strftime: "01/01/2014".
    # We can replace leading zeros for month and day.
    out['dt_strata'] = dates.dt.strftime('%m/%d/%Y').replace(r'^0', '', regex=True).replace(r'/(0\d)/', r'/\1/', regex=True)
    
    # Compute DOW: 0=Sunday, 1=Monday, ..., 6=Saturday
    out['dow'] = dates.dt.dayofweek.astype(int)
    
    # Define mapping for hour columns
    # Source: 1:00 AM, 2:00 AM, ..., 11:00 AM, 12:00 AM, 1:00 PM, ..., 11:00 PM
    # Target: pct_hourly_0100, ..., pct_hourly_2400
    
    # 12:00 AM is Hour 1 (0100)
    # 1:00 AM is Hour 2 (0200)
    # ...
    # 11:00 AM is Hour 11 (1100)
    # 12:00 PM is Hour 12 (1200)
    # 1:00 PM is Hour 13 (1300)
    # ...
    # 11:00 PM is Hour 24 (2400)
    
    hour_mapping = {
        '12:00 AM': 'pct_hourly_0100',
        '1:00 AM': 'pct_hourly_0200',
        '2:00 AM': 'pct_hourly_0300',
        '3:00 AM': 'pct_hourly_0400',
        '4:00 AM': 'pct_hourly_0500',
        '5:00 AM': 'pct_hourly_0600',
        '6:00 AM': 'pct_hourly_0700',
        '7:00 AM': 'pct_hourly_0800',
        '8:00 AM': 'pct_hourly_0900',
        '9:00 AM': 'pct_hourly_1000',
        '10:00 AM': 'pct_hourly_1100',
        '11:00 AM': 'pct_hourly_1200',
        '12:00 PM': 'pct_hourly_1300',
        '1:00 PM': 'pct_hourly_1400',
        '2:00 PM': 'pct_hourly_1500',
        '3:00 PM': 'pct_hourly_1600',
        '4:00 PM': 'pct_hourly_1700',
        '5:00 PM': 'pct_hourly_1800',
        '6:00 PM': 'pct_hourly_1900',
        '7:00 PM': 'pct_hourly_2000',
        '8:00 PM': 'pct_hourly_2100',
        '9:00 PM': 'pct_hourly_2200',
        '10:00 PM': 'pct_hourly_2300',
        '11:00 PM': 'pct_hourly_2400'
    }
    
    # Apply renaming
    for src_col, tgt_col in hour_mapping.items():
        out[tgt_col] = source[src_col]
        
    # Add constant column
    out['pct_hourly_2500'] = 0
    
    # Ensure correct column order
    cols = ['dt_strata', 'dow'] + [f'pct_hourly_{h:02d}00' for h in range(1, 25)] + ['pct_hourly_2500']
    out = out[cols]
    
    return out.reset_index(drop=True)
