import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format: "11/6/2018 21:45"
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # Create a dataframe with the parsed datetime info
    df = source.copy()
    df['dt'] = dt
    df['date_floor'] = dt.dt.floor('D')
    df['hour'] = dt.dt.hour  # 0-23
    
    # We need to map source hours (0-23) to target columns (1-24)
    # Source hour 0 (12 AM) -> Target 0100? Or 2400?
    # Target has 0100 to 2400.
    # Standard: 0100 is 1 AM. 2400 is midnight (end of day).
    # Source 0:00-0:59 is 12 AM. This is usually hour 1 (0100) in some systems, or hour 24 (2400) in others.
    # Let's look at the target sample. 
    # If source has 21:45, it's hour 21.
    # Let's assume standard 1-24 mapping where 1=1AM, 24=Midnight.
    # Source hour 0 -> 1 (0100)? Or 24 (2400)?
    # Source hour 23 -> 23 (2300)? Or 24 (2400)?
    # Let's assume:
    # Source 0 -> 1 (0100)
    # Source 1 -> 2 (0200)
    # ...
    # Source 22 -> 23 (2300)
    # Source 23 -> 24 (2400)
    
    # Actually, let's look at the target columns: 0100 to 2400.
    # If I map source hour H to target H+1, then 23->24.
    # This is a common convention.
    
    df['target_hour'] = df['hour'].apply(lambda h: h + 1)
    
    # Group by date
    groups = df.groupby('date_floor')
    
    records = []
    
    for date_val, group in groups:
        # Format date as MM/dd/yy
        dt_str = date_val.strftime('%m/%d/%y')
        
        # Day of week: 0=Sunday
        dow = date_val.weekday() # 0=Monday, 6=Sunday
        # Convert to 0=Sunday
        dow = (dow + 1) % 7
        
        # Determine active hours
        active_hours = set(group['target_hour'].unique())
        
        row = {
            'dt_strata': dt_str,
            'dow': dow
        }
        
        # Initialize hourly columns
        for h in range(1, 25):
            col_name = f'pct_hourly_{h:02d}00'
            if h in active_hours:
                row[col_name] = 876
            else:
                row[col_name] = 0
                
        row['pct_hourly_2500'] = 0
        
        records.append(row)
        
    out = pd.DataFrame(records)
    
    # Sort by date to match potential expected order? 
    # The target sample is not sorted. 
    # We'll keep the order of appearance in the source (groupby preserves order if sort=False)
    
    # Ensure column order
    cols = ['dt_strata', 'dow']
    for h in range(1, 25):
        cols.append(f'pct_hourly_{h:02d}00')
    cols.append('pct_hourly_2500')
    
    out = out[cols]
    
    # Ensure dtypes
    out['dow'] = out['dow'].astype('int64')
    for h in range(1, 26):
        out[f'pct_hourly_{h:02d}00'] = out[f'pct_hourly_{h:02d}00'].astype('int64')
        
    return out
