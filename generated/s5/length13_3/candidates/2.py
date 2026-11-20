import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Helper to replace 32767 with 0
    def clean_col(col):
        return col.replace(32767, 0)
    
    # Create a copy to avoid modifying source
    df = source.copy()
    
    # Parse timestamp
    df['timestamp_dt'] = pd.to_datetime(df['timestamp'])
    
    # Define aggregation groups
    hvac_cols = [
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    ]
    
    dwh_cols = [
        'WATER HEATER WHS [emon ch7,8]'
    ]
    
    major_appliance_cols = [
        'DRYER WHS (1-CT) [emon ch9]',
        'RANGE WHS (1-CT) [emon ch10]',
        'DISH WASHER WHS [emon ch11]',
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    
    misc_plug_cols = [
        'SPARE1 WHS (1-CT) [emon ch14]',
        'SPARE2 WHS (1-CT) [xpod chA-1]',
        'SPARE3 WHS (1-CT) [xpod chA-2]',
        'SPARE4 WHS (2-CTs) [xpod chA-5,6]'
    ]
    
    total_cols = [
        'TOTAL BLDG WHS [emon ch1,2]'
    ]
    
    # Clean columns
    for col in hvac_cols + dwh_cols + major_appliance_cols + misc_plug_cols + total_cols:
        if col in df.columns:
            df[col] = clean_col(df[col])
            
    # Group by site and timestamp
    grouped = df.groupby(['site', 'timestamp_dt'])
    
    # Aggregate
    agg_df = grouped.agg(
        hvac=('AC COMPRESSOR WHS [emon ch3,4]', 'sum'), # Start with one, then add others
        domestic_water_heating=('WATER HEATER WHS [emon ch7,8]', 'sum'),
        major_appliances=('DRYER WHS (1-CT) [emon ch9]', 'sum'),
        miscellaneous_plug_loads=('SPARE1 WHS (1-CT) [emon ch14]', 'sum'),
        total=('TOTAL BLDG WHS [emon ch1,2]', 'sum')
    ).reset_index()
    
    # Add remaining columns to sums
    # HVAC
    for col in hvac_cols[1:]:
        agg_df['hvac'] = agg_df['hvac'] + df.groupby(['site', 'timestamp_dt'])[col].sum().values
        
    # Major Appliances
    for col in major_appliance_cols[1:]:
        agg_df['major_appliances'] = agg_df['major_appliances'] + df.groupby(['site', 'timestamp_dt'])[col].sum().values
        
    # Misc Plug Loads
    for col in misc_plug_cols[1:]:
        agg_df['miscellaneous_plug_loads'] = agg_df['miscellaneous_plug_loads'] + df.groupby(['site', 'timestamp_dt'])[col].sum().values
        
    # Total
    for col in total_cols[1:]:
        agg_df['total'] = agg_df['total'] + df.groupby(['site', 'timestamp_dt'])[col].sum().values

    # Add lighting column
    agg_df['lighting'] = 0
    
    # Format datetime
    agg_df['datetime'] = agg_df['timestamp_dt'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Select and rename columns
    result = agg_df[['datetime', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    # Ensure dtypes match target
    result['hvac'] = result['hvac'].astype('int64')
    result['domestic_water_heating'] = result['domestic_water_heating'].astype('int64')
    result['major_appliances'] = result['major_appliances'].astype('int64')
    result['lighting'] = result['lighting'].astype('int64')
    result['miscellaneous_plug_loads'] = result['miscellaneous_plug_loads'].astype('float64')
    result['total'] = result['total'].astype('int64')
    
    return result
