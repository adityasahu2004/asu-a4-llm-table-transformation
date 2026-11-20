import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Replace sensor error value 32767 with 0
    df = source.replace(32767.0, 0.0)
    
    # Parse timestamp
    df['timestamp_dt'] = pd.to_datetime(df['timestamp'])
    
    # Define column mappings for aggregation
    # HVAC: AC Compressor + Air Handler + Minisplit
    hvac_cols = [
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    ]
    
    # Domestic Water Heating
    dwh_cols = [
        'WATER HEATER WHS [emon ch7,8]'
    ]
    
    # Major Appliances: Dryer(1-CT), Range, Dishwasher, Primary Fridge, 2nd Fridge, Dryer(2-CTs)
    major_cols = [
        'DRYER WHS (1-CT) [emon ch9]',
        'RANGE WHS (1-CT) [emon ch10]',
        'DISH WASHER WHS [emon ch11]',
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    
    # Miscellaneous Plug Loads: Calculated Unmeasured loads
    misc_cols = [
        'Calculated Unmeasured loads (Whr)'
    ]
    
    # Total: Total Bldg WHS
    total_cols = [
        'TOTAL BLDG WHS [emon ch1,2]'
    ]
    
    # Calculate sums per row
    df['hvac_sum'] = df[hvac_cols].sum(axis=1)
    df['dwh_sum'] = df[dwh_cols].sum(axis=1)
    df['major_sum'] = df[major_cols].sum(axis=1)
    df['misc_sum'] = df[misc_cols].sum(axis=1)
    df['total_sum'] = df[total_cols].sum(axis=1)
    
    # Group by timestamp and sum across sites
    grouped = df.groupby('timestamp_dt').agg(
        hvac_sum=('hvac_sum', 'sum'),
        dwh_sum=('dwh_sum', 'sum'),
        major_sum=('major_sum', 'sum'),
        misc_sum=('misc_sum', 'sum'),
        total_sum=('total_sum', 'sum')
    ).reset_index()
    
    # Convert to target units (multiply by 3600)
    # HVAC, DWH, Major, Total are int64 in target
    # Misc is float64 in target
    
    result = pd.DataFrame()
    result['datetime'] = grouped['timestamp_dt'].dt.strftime('%Y-%m-%d %H:%M:%S')
    result['hvac'] = (grouped['hvac_sum'] * 3600).astype('int64')
    result['domestic_water_heating'] = (grouped['dwh_sum'] * 3600).astype('int64')
    result['major_appliances'] = (grouped['major_sum'] * 3600).astype('int64')
    result['lighting'] = 0
    result['miscellaneous_plug_loads'] = grouped['misc_sum'] * 3600
    result['total'] = (grouped['total_sum'] * 3600).astype('int64')
    
    return result
