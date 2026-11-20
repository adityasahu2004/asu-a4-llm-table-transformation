import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format observed: M/D/YYYY e.g., "7/3/2014"
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create dt_strata: M/D/YYYY
    # Note: pd.strftime('%-m/%-d/%Y') works on Linux/macOS. For cross-platform safety with non-zero padding:
    # We can use .dt.strftime('%m/%d/%Y') and then strip leading zeros, or rely on specific pandas behavior.
    # Standard %m is zero-padded. The target shows "1/1/2014".
    # Let's use a lambda or string replacement to ensure no leading zeros if %m produces them.
    dt_strata = dates.dt.strftime('%m/%d/%Y').str.lstrip('0').replace('0/', '/', regex=False).replace('0', '0', regex=False) 
    # The above regex replacement is messy. Better approach:
    # dt.strftime('%-m/%-d/%Y') is not cross-platform.
    # Let's just use %m/%d/%Y and remove leading zeros from month and day parts.
    dt_strata = dates.apply(lambda x: f"{x.month}/{x.day}/{x.year}")
    
    # Calculate dow: Monday=0 ... Sunday=6
    dow = dates.dt.dayofweek
    
    # Map hourly columns
    # Source: 1:00 AM ... 12:00 PM
    # Target: pct_hourly_0100 ... pct_hourly_2400
    
    out = pd.DataFrame()
    out['dt_strata'] = dt_strata
    out['dow'] = dow
    
    # Mapping logic:
    # 1:00 AM -> 0100
    # 2:00 AM -> 0200
    # ...
    # 11:00 AM -> 1100
    # 12:00 PM -> 1200
    # 1:00 PM -> 1300
    # ...
    # 11:00 PM -> 2300
    # 12:00 AM -> 2400
    
    mapping = {
        '1:00 AM': 'pct_hourly_0100',
        '2:00 AM': 'pct_hourly_0200',
        '3:00 AM': 'pct_hourly_0300',
        '4:00 AM': 'pct_hourly_0400',
        '5:00 AM': 'pct_hourly_0500',
        '6:00 AM': 'pct_hourly_0600',
        '7:00 AM': 'pct_hourly_0700',
        '8:00 AM': 'pct_hourly_0800',
        '9:00 AM': 'pct_hourly_0900',
        '10:00 AM': 'pct_hourly_1000',
        '11:00 AM': 'pct_hourly_1100',
        '12:00 PM': 'pct_hourly_1200',
        '1:00 PM': 'pct_hourly_1300',
        '2:00 PM': 'pct_hourly_1400',
        '3:00 PM': 'pct_hourly_1500',
        '4:00 PM': 'pct_hourly_1600',
        '5:00 PM': 'pct_hourly_1700',
        '6:00 PM': 'pct_hourly_1800',
        '7:00 PM': 'pct_hourly_1900',
        '8:00 PM': 'pct_hourly_2000',
        '9:00 PM': 'pct_hourly_2100',
        '10:00 PM': 'pct_hourly_2200',
        '11:00 PM': 'pct_hourly_2300',
        '12:00 AM': 'pct_hourly_2400',
    }
    
    for src_col, tgt_col in mapping.items():
        out[tgt_col] = source[src_col]
        
    out['pct_hourly_2500'] = 0
    
    return out
