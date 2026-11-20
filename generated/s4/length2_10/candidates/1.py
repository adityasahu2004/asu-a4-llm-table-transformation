import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format in sample: "11/6/2018 21:45"
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date and hour
    df['date_only'] = df['dt'].dt.date
    df['hour'] = df['dt'].dt.hour
    
    # We need to count non-null values of zone_016_cooling_sp per date and hour
    # The target columns are pct_hourly_0100 to pct_hourly_2400
    # Hour 0 in pandas is 0:00-0:59. This maps to "Hour 24" or "Hour 00"?
    # Standard 24-hour clock: 0-23.
    # Target columns: 0100, 0200, ... 2400.
    # Usually:
    # 01:00 -> Hour 1 (1:00-1:59)
    # ...
    # 23:00 -> Hour 23 (23:00-23:59)
    # 24:00 -> Hour 24 (0:00-0:59 of the next day? Or 0:00-0:59 of the same day?)
    # In many energy datasets, 24:00 represents the midnight hour (0:00-0:59).
    # Let's assume:
    # Hour 1 = 1:00-1:59
    # ...
    # Hour 23 = 23:00-23:59
    # Hour 24 = 0:00-0:59
    
    # Let's verify with the sample if possible. 
    # Sample source: 11/6/2018 21:45. Hour 21.
    # If this maps to pct_hourly_2100, then Hour 21 is 21:00-21:59.
    # What about 0:00? It maps to pct_hourly_2400.
    
    # Create a mapping for hour bins
    # pandas hour: 0..23
    # target col: 1..23, 24
    # pandas 0 -> target 24
    # pandas 1 -> target 1
    # ...
    # pandas 23 -> target 23
    
    def get_hour_col(h):
        if h == 0:
            return 'pct_hourly_2400'
        else:
            return f'pct_hourly_{h:02d}00'

    # Group by date and hour, count non-nulls
    # We need to drop nulls in the value column first to count correctly
    valid_df = df.dropna(subset=['zone_016_cooling_sp'])
    
    # Group by date and hour
    counts = valid_df.groupby(['date_only', 'hour']).size().reset_index(name='count')
    
    # Pivot to wide format
    pivot = counts.pivot_table(index='date_only', columns='hour', values='count', fill_value=0)
    
    # Prepare the result dataframe
    # We need to ensure all hours 0-23 are present in the pivot for every date
    all_hours = list(range(0, 24))
    pivot = pivot.reindex(columns=all_hours, fill_value=0)
    
    # Map hours to target column names
    # Create a new dataframe
    res = pd.DataFrame(index=pivot.index)
    
    for h in range(0, 24):
        col_name = get_hour_col(h)
        res[col_name] = pivot[h].astype(int)
        
    # Add pct_hourly_2500 as 0
    res['pct_hourly_2500'] = 0
    
    # Add dt_strata and dow
    # dt_strata format: MM/DD/YY
    res['dt_strata'] = res.index.strftime('%m/%d/%y')
    
    # dow: 0=Monday, 6=Sunday (standard pandas weekday)
    # The target distinct values are 0-6.
    res['dow'] = res.index.weekday
    
    # Select and order columns
    cols = ['dt_strata', 'dow']
    for h in range(1, 25):
        cols.append(f'pct_hourly_{h:02d}00')
        
    res = res[cols]
    
    # Reset index to clean up
    res = res.reset_index(drop=True)
    
    return res
