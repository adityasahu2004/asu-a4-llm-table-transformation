import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Identify bad data rows where sensors report 32767.0
    bad_val = 32767.0
    
    # Filter out rows where any of the main energy columns are bad
    # We check a representative set of columns that are likely to be bad if the row is bad
    cols_to_check = [
        'TOTAL BLDG WHS [emon ch1,2]',
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'WATER HEATER WHS [emon ch7,8]',
        'DRYER WHS (1-CT) [emon ch9]',
        'RANGE WHS (1-CT) [emon ch10]',
        'DISH WASHER WHS [emon ch11]',
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]',
        'SPARE1 WHS (1-CT) [emon ch14]',
        'SPARE2 WHS (1-CT) [xpod chA-1]',
        'SPARE3 WHS (1-CT) [xpod chA-2]',
        'POOL PUMP WHS (2-CTs) [xpod chA-3,4]',
        'SPARE4 WHS (2-CTs) [xpod chA-5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    
    # Create a mask for valid rows (none of the checked columns are 32767.0)
    valid_mask = True
    for col in cols_to_check:
        if col in source.columns:
            valid_mask = valid_mask & (source[col] != bad_val)
            
    df = source[valid_mask].copy()
    
    # Parse timestamp
    df['timestamp_dt'] = pd.to_datetime(df['timestamp'])
    df['month'] = df['timestamp_dt'].dt.month
    df['hour'] = df['timestamp_dt'].dt.hour
    
    # Define category sums
    # HVAC
    hvac_cols = [
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    ]
    df['HVAC'] = df[hvac_cols].sum(axis=1)
    
    # Domestic Water Heating
    df['domestic_water_heating'] = df['WATER HEATER WHS [emon ch7,8]']
    
    # Major Appliances
    major_appliance_cols = [
        'DRYER WHS (1-CT) [emon ch9]',
        'RANGE WHS (1-CT) [emon ch10]',
        'DISH WASHER WHS [emon ch11]',
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    df['major_appliances'] = df[major_appliance_cols].sum(axis=1)
    
    # Lighting (Constant 0)
    df['lighting'] = 0
    
    # Miscellaneous Plug Loads
    misc_cols = [
        'SPARE1 WHS (1-CT) [emon ch14]',
        'SPARE2 WHS (1-CT) [xpod chA-1]',
        'SPARE3 WHS (1-CT) [xpod chA-2]',
        'SPARE4 WHS (2-CTs) [xpod chA-5,6]',
        'POOL PUMP WHS (2-CTs) [xpod chA-3,4]'
    ]
    df['miscellaneous_plug_loads'] = df[misc_cols].sum(axis=1)
    
    # Total
    df['Total'] = df['TOTAL BLDG WHS [emon ch1,2]']
    
    # Group by month and hour and sum
    agg_df = df.groupby(['month', 'hour']).agg(
        HVAC=('HVAC', 'sum'),
        domestic_water_heating=('domestic_water_heating', 'sum'),
        major_appliances=('major_appliances', 'sum'),
        lighting=('lighting', 'sum'),
        miscellaneous_plug_loads=('miscellaneous_plug_loads', 'sum'),
        Total=('Total', 'sum')
    ).reset_index()
    
    # Cast types to match target exactly
    agg_df['HVAC'] = agg_df['HVAC'].astype('int64')
    agg_df['domestic_water_heating'] = agg_df['domestic_water_heating'].astype('int64')
    agg_df['major_appliances'] = agg_df['major_appliances'].astype('int64')
    agg_df['lighting'] = agg_df['lighting'].astype('int64')
    agg_df['miscellaneous_plug_loads'] = agg_df['miscellaneous_plug_loads'].astype('float64')
    agg_df['Total'] = agg_df['Total'].astype('int64')
    
    # Ensure column order
    result = agg_df[['month', 'hour', 'HVAC', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'Total']]
    
    return result
