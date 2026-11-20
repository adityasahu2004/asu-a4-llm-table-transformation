import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    df['date_only'] = df['dt'].dt.normalize()
    df['hour'] = df['dt'].dt.hour

    # Map hour 0-23 to hour labels 1-24
    # Hour 0 (midnight) -> Hour 1 (01:00 bin)
    # Hour 1 -> Hour 2
    # ...
    # Hour 23 -> Hour 24
    df['hour_bin'] = df['hour'] + 1

    # Group by date and hour_bin, take mean of cerc_logger_1
    grouped = df.groupby(['date_only', 'hour_bin'])['cerc_logger_1'].mean().unstack(fill_value=0.0)

    # Ensure all 24 columns exist
    for h in range(1, 25):
        if h not in grouped.columns:
            grouped[h] = 0.0

    # Sort columns by hour
    grouped = grouped[[h for h in range(1, 25)]]

    # Build output dataframe
    out = pd.DataFrame(index=grouped.index)
    out.index.name = None
    
    # Format date as MM/DD/YY
    out['dt_strata'] = grouped.index.strftime('%m/%d/%y')
    
    # Day of week: 0=Monday, ..., 6=Sunday
    out['dow'] = grouped.index.dayofweek.astype(int)
    
    # Map hour bins to target column names
    for h in range(1, 25):
        out[f'pct_hourly_{h:02d}00'] = grouped[h].astype(float)
    
    out['pct_hourly_2500'] = 0

    return out.reset_index(drop=True)
