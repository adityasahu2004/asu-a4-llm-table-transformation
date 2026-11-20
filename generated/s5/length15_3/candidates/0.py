import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    source = source.copy()
    source['timestamp'] = pd.to_datetime(source['timestamp'])
    
    # Extract hour and season
    source['hour'] = source['timestamp'].dt.hour
    source['month'] = source['timestamp'].dt.month
    
    # Define season
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
            
    source['season'] = source['month'].apply(get_season)
    
    # Define columns for each category
    hvac_cols = ['AC COMPRESSOR WHS [emon ch3,4]', 'AIR HANDLER WHS [emon ch5,6]']
    dwh_cols = ['WATER HEATER WHS [emon ch7,8]']
    major_appl_cols = ['DRYER WHS (1-CT) [emon ch9]', 'RANGE WHS (1-CT) [emon ch10]', 
                       'DISH WASHER WHS [emon ch11]', 'Primary Fridge WHS [emon ch12]', 
                       '2nd Fridge WHS [emon ch13]']
    misc_plug_cols = ['SPARE1 WHS (1-CT) [emon ch14]', 'SPARE2 WHS (1-CT) [xpod chA-1]', 
                      'SPARE3 WHS (1-CT) [xpod chA-2]', 'POOL PUMP WHS (2-CTs) [xpod chA-3,4]', 
                      'SPARE4 WHS (2-CTs) [xpod chA-5,6]', 'Minisplit WHS (2-CTs) [xpod chA-7,8]', 
                      'Dryer WHS (2-CTs) [xpod chA-9,10]']
    total_col = 'TOTAL BLDG WHS [emon ch1,2]'
    
    # Calculate sums for each category
    source['HVAC'] = source[hvac_cols].sum(axis=1)
    source['domestic_water_heating'] = source[dwh_cols].sum(axis=1)
    source['major_appliances'] = source[major_appl_cols].sum(axis=1)
    source['miscellaneous_plug_loads'] = source[misc_plug_cols].sum(axis=1)
    source['Total'] = source[total_col]
    source['lighting'] = 0
    
    # Group by season and hour, then sum
    result = source.groupby(['season', 'hour']).agg({
        'HVAC': 'sum',
        'domestic_water_heating': 'sum',
        'major_appliances': 'sum',
        'lighting': 'sum',
        'miscellaneous_plug_loads': 'sum',
        'Total': 'sum'
    }).reset_index()
    
    # Cast types to match target
    result['HVAC'] = result['HVAC'].astype('int64')
    result['domestic_water_heating'] = result['domestic_water_heating'].astype('int64')
    result['major_appliances'] = result['major_appliances'].astype('int64')
    result['lighting'] = result['lighting'].astype('int64')
    result['Total'] = result['Total'].astype('int64')
    # miscellaneous_plug_loads remains float64
    
    # Sort by season and hour to match typical output order (though target sample is not sorted)
    # The target sample seems to be in a specific order. Let's just return the grouped result.
    # The target sample has Summer 19, Fall 2, Summer 3, Spring 8, Spring 7, Summer 14, Spring 4, Summer 15, Fall 17, Fall 5, Winter 2, Winter 18.
    # This is not sorted. It might be the order of appearance in the source or random.
    # We will just return the grouped dataframe.
    
    return result[['season', 'hour', 'HVAC', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'Total']]
