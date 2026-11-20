import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    source['dt'] = pd.to_datetime(source['timestamp'])
    source['month'] = source['dt'].dt.month
    source['hour'] = source['dt'].dt.hour
    
    # Define columns for each category
    hvac_cols = [
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]'
    ]
    
    water_cols = [
        'WATER HEATER WHS [emon ch7,8]'
    ]
    
    major_cols = [
        'DRYER WHS (1-CT) [emon ch9]',
        'RANGE WHS (1-CT) [emon ch10]',
        'DISH WASHER WHS [emon ch11]',
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    
    # Lighting is 0
    
    # Miscellaneous Plug Loads: 
    # Based on float dtype in target, and source 'Calculated Unmeasured loads' having decimals,
    # and 'Spare' columns being integers, we map 'Calculated Unmeasured loads' to misc.
    # Alternatively, if 'Minisplit' is considered misc, it's integer.
    # Let's stick with 'Calculated Unmeasured loads (Whr)' for the float characteristic.
    misc_cols = [
        'Calculated Unmeasured loads (Whr)'
    ]
    
    # Total: Use TOTAL BLDG WHS
    total_col = 'TOTAL BLDG WHS [emon ch1,2]'
    
    # Filter out invalid data (32767 is a common sentinel for missing/bad data in emon/wattsup)
    # We check the total column for validity
    valid_mask = source[total_col] != 32767.0
    
    df_valid = source[valid_mask].copy()
    
    # Calculate component sums
    df_valid['HVAC'] = df_valid[hvac_cols].sum(axis=1)
    df_valid['domestic_water_heating'] = df_valid[water_cols].sum(axis=1)
    df_valid['major_appliances'] = df_valid[major_cols].sum(axis=1)
    df_valid['lighting'] = 0
    df_valid['miscellaneous_plug_loads'] = df_valid[misc_cols].sum(axis=1)
    df_valid['Total'] = df_valid[total_col]
    
    # Aggregate by month and hour
    agg_df = df_valid.groupby(['month', 'hour'], as_index=False).agg(
        HVAC=('HVAC', 'sum'),
        domestic_water_heating=('domestic_water_heating', 'sum'),
        major_appliances=('major_appliances', 'sum'),
        lighting=('lighting', 'sum'),
        miscellaneous_plug_loads=('miscellaneous_plug_loads', 'sum'),
        Total=('Total', 'sum')
    )
    
    # Ensure correct dtypes
    agg_df['HVAC'] = agg_df['HVAC'].astype('int64')
    agg_df['domestic_water_heating'] = agg_df['domestic_water_heating'].astype('int64')
    agg_df['major_appliances'] = agg_df['major_appliances'].astype('int64')
    agg_df['lighting'] = agg_df['lighting'].astype('int64')
    # miscellaneous_plug_loads stays float64
    agg_df['Total'] = agg_df['Total'].astype('int64')
    
    # Sort to match potential expected order (not strictly required but good practice)
    agg_df = agg_df.sort_values(['month', 'hour']).reset_index(drop=True)
    
    return agg_df
