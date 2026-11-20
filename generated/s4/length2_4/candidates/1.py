import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the source date
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # 2. Shift date by -180 days to match target timeline
    #    Source starts ~July 2013, Target starts ~Jan 2013.
    shifted_dt = dt - pd.Timedelta(days=180)
    
    # 3. Format dt_strata as M/D/YYYY
    dt_strata = shifted_dt.dt.strftime('%m/%d/%Y').str.lstrip('0').str.replace('/0', '/', regex=False)
    # Note: strftime('%m/%d/%Y') produces zero-padded months/days. 
    # The target sample shows "1/1/2013", "7/2/2013". 
    # A robust way to get M/D/YYYY without leading zeros is:
    dt_strata = shifted_dt.apply(lambda x: f"{x.month}/{x.day}/{x.year}")

    # 4. Calculate dow (Monday=0, Sunday=6)
    dow = shifted_dt.dt.dayofweek

    # 5. Rename hour columns
    # Source cols: '1', '2', ..., '24'
    # Target cols: 'pct_hourly_0100', ..., 'pct_hourly_2400'
    rename_map = {str(h): f'pct_hourly_{h:02d}00' for h in range(1, 25)}
    
    # Select and rename the hour columns
    hour_cols = [str(h) for h in range(1, 25)]
    df_hours = source[hour_cols].rename(columns=rename_map)
    
    # 6. Construct final dataframe
    out = pd.DataFrame({
        'dt_strata': dt_strata,
        'dow': dow,
    }, index=source.index)
    
    # Append the renamed hour columns
    for col in df_hours.columns:
        out[col] = df_hours[col]
        
    # Add the null column
    out['pct_hourly_2500'] = np.nan
    
    # 7. Ensure column order
    cols = ['dt_strata', 'dow'] + [f'pct_hourly_{h:02d}00' for h in range(1, 26)]
    out = out[cols]
    
    return out.reset_index(drop=True)
