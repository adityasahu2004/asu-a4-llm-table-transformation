import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    df = source.copy()
    df['timestamp_dt'] = pd.to_datetime(df['timestamp'])
    
    # Filter out invalid rows marked by 32767 in Total
    total_col = 'TOTAL BLDG WHS [emon ch1,2]'
    df = df[df[total_col] != 32767].copy()
    
    # Derive season and hour
    months = df['timestamp_dt'].dt.month
    def get_season(m):
        if m in [12, 1, 2]:
            return 'Winter'
        elif m in [3, 4, 5]:
            return 'Spring'
        elif m in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
            
    df['season'] = months.apply(get_season)
    df['hour'] = df['timestamp_dt'].dt.hour
    
    # Helper to clean 32767 values
    def clean_col(col_name):
        return df[col_name].replace(32767, 0)

    # HVAC: AC Compressor + Air Handler + Minisplit
    hvac_cols = [
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    ]
    df['HVAC'] = sum(clean_col(c) for c in hvac_cols)
    
    # Domestic Water Heating
    df['domestic_water_heating'] = clean_col('WATER HEATER WHS [emon ch7,8]')
    
    # Major Appliances: Dryer(1-CT), Range, Dish Washer, Primary Fridge, 2nd Fridge, Dryer(2-CTs)
    major_appl_cols = [
        'DRYER WHS (1-CT) [emon ch9]',
        'RANGE WHS (1-CT) [emon ch10]',
        'DISH WASHER WHS [emon ch11]',
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    df['major_appliances'] = sum(clean_col(c) for c in major_appl_cols)
    
    # Lighting: Constant 0
    df['lighting'] = 0
    
    # Miscellaneous Plug Loads: Spare1, Spare2, Spare3, Spare4, Pool Pump
    misc_cols = [
        'SPARE1 WHS (1-CT) [emon ch14]',
        'SPARE2 WHS (1-CT) [xpod chA-1]',
        'SPARE3 WHS (1-CT) [xpod chA-2]',
        'SPARE4 WHS (2-CTs) [xpod chA-5,6]',
        'POOL PUMP WHS (2-CTs) [xpod chA-3,4]'
    ]
    df['miscellaneous_plug_loads'] = sum(clean_col(c) for c in misc_cols)
    
    # Total
    df['Total'] = df[total_col]
    
    # Group by season and hour
    grouped = df.groupby(['season', 'hour']).agg(
        HVAC=('HVAC', 'sum'),
        domestic_water_heating=('domestic_water_heating', 'sum'),
        major_appliances=('major_appliances', 'sum'),
        lighting=('lighting', 'sum'),
        miscellaneous_plug_loads=('miscellaneous_plug_loads', 'sum'),
        Total=('Total', 'sum')
    ).reset_index()
    
    # Cast types
    grouped['HVAC'] = grouped['HVAC'].astype('int64')
    grouped['domestic_water_heating'] = grouped['domestic_water_heating'].astype('int64')
    grouped['major_appliances'] = grouped['major_appliances'].astype('int64')
    grouped['lighting'] = grouped['lighting'].astype('int64')
    grouped['Total'] = grouped['Total'].astype('int64')
    # miscellaneous_plug_loads remains float64 as per target schema
    
    # Sort by season order and hour
    season_order = {'Winter': 0, 'Spring': 1, 'Summer': 2, 'Fall': 3}
    grouped['season_sort'] = grouped['season'].map(season_order)
    grouped = grouped.sort_values(['season_sort', 'hour']).drop(columns=['season_sort'])
    
    return grouped[['season', 'hour', 'HVAC', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'Total']]
