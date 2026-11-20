import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Format dt_strata as M/D/YYYY
    out['dt_strata'] = dt.dt.strftime('%-m/%-d/%Y')
    
    # Calculate dow (0=Monday, 6=Sunday)
    out['dow'] = dt.dt.dayofweek
    
    # Map hourly columns
    # Source columns: 1:00 AM, 2:00 AM, ..., 11:00 AM, 12:00 PM, 1:00 PM, ..., 11:00 PM, 12:00 AM
    # Target columns: pct_hourly_0100, ..., pct_hourly_1100, pct_hourly_1200, pct_hourly_1300, ..., pct_hourly_2300, pct_hourly_2400
    
    # Define mapping
    hour_map = {
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
        '12:00 AM': 'pct_hourly_2400'
    }
    
    for src_col, tgt_col in hour_map.items():
        out[tgt_col] = source[src_col]
        
    # Add constant column
    out['pct_hourly_2500'] = 0
    
    return out.reset_index(drop=True)
