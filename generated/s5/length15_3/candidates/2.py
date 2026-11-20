import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    df = source.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Extract hour and month
    df['hour'] = df['timestamp'].dt.hour
    df['month'] = df['timestamp'].dt.month
    
    # Determine season
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
            
    df['season'] = df['month'].apply(get_season)
    
    # Define column groups
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
    
    misc_cols = [
        'SPARE1 WHS (1-CT) [emon ch14]',
        'SPARE2 WHS (1-CT) [xpod chA-1]',
        'SPARE3 WHS (1-CT) [xpod chA-2]',
        'POOL PUMP WHS (2-CTs) [xpod chA-3,4]',
        'SPARE4 WHS (2-CTs) [xpod chA-5,6]',
        'Calculated Unmeasured loads (Whr)'
    ]
    
    total_col = 'TOTAL BLDG WHS [emon ch1,2]'
    
    # Calculate sums for each group
    df['HVAC'] = df[hvac_cols].sum(axis=1)
    df['domestic_water_heating'] = df[dwh_cols].sum(axis=1)
    df['major_appliances'] = df[major_appliance_cols].sum(axis=1)
    df['miscellaneous_plug_loads'] = df[misc_cols].sum(axis=1)
    df['Total'] = df[total_col]
    
    # Group by season and hour and sum the aggregated values
    agg_df = df.groupby(['season', 'hour']).agg(
        HVAC=('HVAC', 'sum'),
        domestic_water_heating=('domestic_water_heating', 'sum'),
        major_appliances=('major_appliances', 'sum'),
        miscellaneous_plug_loads=('miscellaneous_plug_loads', 'sum'),
        Total=('Total', 'sum')
    ).reset_index()
    
    # Add lighting column
    agg_df['lighting'] = 0
    
    # Reorder columns to match target
    agg_df = agg_df[['season', 'hour', 'HVAC', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'Total']]
    
    # Convert types
    agg_df['HVAC'] = agg_df['HVAC'].astype('int64')
    agg_df['domestic_water_heating'] = agg_df['domestic_water_heating'].astype('int64')
    agg_df['major_appliances'] = agg_df['major_appliances'].astype('int64')
    agg_df['lighting'] = agg_df['lighting'].astype('int64')
    agg_df['Total'] = agg_df['Total'].astype('int64')
    # miscellaneous_plug_loads remains float
    
    return agg_df
