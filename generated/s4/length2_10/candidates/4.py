import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    df['date_only'] = df['dt'].dt.date
    df['hour'] = df['dt'].dt.hour
    
    # Group by date and hour, sum the cooling setpoint
    grouped = df.groupby(['date_only', 'hour'])['zone_016_cooling_sp'].sum().reset_index()
    
    # Pivot to get one row per date, one column per hour
    pivoted = grouped.pivot_table(index='date_only', columns='hour', values='zone_016_cooling_sp', fill_value=0)
    
    # Rename columns to match target
    # Hour 0 -> pct_hourly_0100
    # Hour 1 -> pct_hourly_0200
    # ...
    # Hour 23 -> pct_hourly_2400
    pivoted.columns = [f'pct_hourly_{h+1:02d}00' for h in pivoted.columns]
    
    # Add pct_hourly_2500
    pivoted['pct_hourly_2500'] = 0
    
    # Add dt_strata and dow
    pivoted['dt_strata'] = pd.to_datetime(pivoted.index).dt.strftime('%m/%d/%y')
    pivoted['dow'] = pd.to_datetime(pivoted.index).dt.strftime('%w').astype(int)
    
    # Reset index and reorder columns
    pivoted = pivoted.reset_index(drop=True)
    cols = ['dt_strata', 'dow'] + [f'pct_hourly_{h:02d}00' for h in range(1, 26)]
    pivoted = pivoted[cols]
    
    return pivoted
