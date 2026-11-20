import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    source = source.copy()
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date for grouping
    source['date_only'] = source['dt'].dt.date
    
    # Group by date and sum the cooling setpoint
    # The target values (876, 657) correspond to sums of 73.0 (12*73=876, 9*73=657)
    daily_sum = source.groupby('date_only')['zone_016_cooling_sp'].sum().reset_index()
    daily_sum.columns = ['date_only', 'daily_total']
    
    # Create the output dataframe
    out = pd.DataFrame()
    out['dt_strata'] = pd.to_datetime(daily_sum['date_only']).dt.strftime('%m/%d/%y')
    
    # Calculate dow: Sunday=0, Monday=1, ..., Saturday=6
    # Python weekday: Mon=0, ..., Sun=6
    # Formula: (weekday + 1) % 7
    dt_series = pd.to_datetime(daily_sum['date_only'])
    out['dow'] = (dt_series.dt.weekday + 1) % 7
    
    # Create hourly columns 0100 to 2400 with the daily total
    for h in range(1, 25):
        out[f'pct_hourly_{h:02d}00'] = daily_sum['daily_total']
        
    # Add the 2500 column with 0
    out['pct_hourly_2500'] = 0
    
    # Ensure integer types for the hourly columns as per target schema
    for col in out.columns:
        if col.startswith('pct_hourly'):
            out[col] = out[col].astype('int64')
            
    return out
