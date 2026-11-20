import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    src = source.copy()
    src['dt'] = pd.to_datetime(src['date'])
    src['date_only'] = src['dt'].dt.date
    src['hour'] = src['dt'].dt.hour
    
    # Map hour 0 to 24, others stay same. 
    # We need columns 1..24.
    # Hour 0 -> 24
    # Hour 1 -> 1
    # ...
    # Hour 23 -> 23
    
    def map_hour(h):
        if h == 0:
            return 24
        return h
        
    src['hour_idx'] = src['hour'].apply(map_hour)
    
    # Pivot
    # We want one row per date_only
    # Columns: 1..24
    
    pivot_data = src.groupby(['date_only', 'hour_idx'])['zone_016'].first().unstack(fill_value=0.0)
    
    # Ensure all hours 1-24 exist
    for h in range(1, 25):
        if h not in pivot_data.columns:
            pivot_data[h] = 0.0
            
    # Sort columns
    pivot_data = pivot_data.sort_index(axis=1)
    
    # Create output dataframe
    out = pd.DataFrame(index=pivot_data.index)
    
    # dt_strata: MM/DD/YY
    out['dt_strata'] = pd.to_datetime(pivot_data.index).strftime('%m/%d/%y')
    
    # dow: 1=Mon ... 7=Sun
    out['dow'] = pd.to_datetime(pivot_data.index).dayofweek + 1
    
    # Hourly columns
    for h in range(1, 25):
        out[f'pct_hourly_{h:02d}00'] = pivot_data[h]
        
    # pct_hourly_2500 is always 0
    out['pct_hourly_2500'] = 0
    
    # Sort by dt_strata? The sample shows 01/02/18 then 01/01/18. 
    # Let's check the order in sample.
    # Sample: 
    # 01/02/18, 2
    # 01/01/18, 1
    # This looks like it might be sorted by date descending or just input order?
    # The source dates are:
    # 1/2/2018 ...
    # 1/3/2018 ...
    # The target has 01/02/18 first, then 01/01/18.
    # Wait, the source sample has:
    # 1/2/2018 0:11
    # ...
    # 1/3/2018 0:20
    # But the target distinct values are 01/02/18 and 01/01/18.
    # Where did 01/01/18 come from?
    # The source sample only shows 1/2 and 1/3.
    # However, the note says "Source row count describes a training sample only".
    # The target sample has 2 rows.
    # Let's assume the standard behavior is to sort by date ascending or preserve groupby order.
    # The target sample order: 01/02/18, then 01/01/18.
    # If I sort by dt_strata ascending: 01/01/18, 01/02/18.
    # If I sort by dt_strata descending: 01/02/18, 01/01/18.
    # The target sample shows descending order.
    
    out = out.reset_index(drop=True)
    # Sort descending by dt_strata to match sample order?
    # Or maybe it's just arbitrary?
    # Let's sort descending by date to be safe given the sample.
    out['dt_obj'] = pd.to_datetime(out['dt_strata'])
    out = out.sort_values('dt_obj', ascending=False).drop('dt_obj', axis=1).reset_index(drop=True)
    
    return out
