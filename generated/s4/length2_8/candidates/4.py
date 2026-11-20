import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    df['date_only'] = df['dt'].dt.normalize()
    df['hour'] = df['dt'].dt.hour + 1  # 1-24

    # Aggregate by date and hour
    agg = df.groupby(['date_only', 'hour'])['cerc_logger_1'].mean().reset_index()

    # Pivot to wide
    pivoted = agg.pivot(index='date_only', columns='hour', values='cerc_logger_1')

    # Ensure all hours 1-24 are present, fill NaN with 0
    for h in range(1, 25):
        if h not in pivoted.columns:
            pivoted[h] = 0.0
    pivoted = pivoted[[h for h in range(1, 25)]].fillna(0.0)

    # Reset index to make date_only a column
    pivoted = pivoted.reset_index()

    # Format date column
    out = pd.DataFrame()
    out['dt_strata'] = pivoted['date_only'].dt.strftime('%m/%d/%y')
    out['dow'] = pivoted['date_only'].dt.dayofweek + 1  # Mon=1, Sun=7

    # Map hours 1-24 to target columns
    for h in range(1, 25):
        out[f'pct_hourly_{h:02d}00'] = pivoted[h]

    # Add constant 0 column for hour 25
    out['pct_hourly_2500'] = 0

    return out
