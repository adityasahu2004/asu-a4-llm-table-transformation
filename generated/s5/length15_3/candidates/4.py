import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    df = source.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Filter out invalid rows where total building load is sentinel 32767
    valid_mask = df['TOTAL BLDG WHS [emon ch1,2]'] != 32767.0
    df = df[valid_mask]
    
    # Derive season
    months = df['timestamp'].dt.month
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
    
    # Derive hour
    df['hour'] = df['timestamp'].dt.hour
    
    # Define component sums
    # HVAC: AC Compressor + Air Handler + Minisplit
    df['HVAC'] = (df['AC COMPRESSOR WHS [emon ch3,4]'] + 
                  df['AIR HANDLER WHS [emon ch5,6]'] + 
                  df['Minisplit WHS (2-CTs) [xpod chA-7,8]'])
    
    # Domestic Water Heating
    df['domestic_water_heating'] = df['WATER HEATER WHS [emon ch7,8]']
    
    # Major Appliances: Dryer(1-CT) + Range + Dishwasher + Primary Fridge + 2nd Fridge + Dryer(2-CT)
    df['major_appliances'] = (df['DRYER WHS (1-CT) [emon ch9]'] + 
                              df['RANGE WHS (1-CT) [emon ch10]'] + 
                              df['DISH WASHER WHS [emon ch11]'] + 
                              df['Primary Fridge WHS [emon ch12]'] + 
                              df['2nd Fridge WHS [emon ch13]'] + 
                              df['Dryer WHS (2-CTs) [xpod chA-9,10]'])
    
    # Lighting: 0
    df['lighting'] = 0
    
    # Miscellaneous Plug Loads: Spares + Calculated Unmeasured
    df['miscellaneous_plug_loads'] = (df['SPARE1 WHS (1-CT) [emon ch14]'] + 
                                      df['SPARE2 WHS (1-CT) [xpod chA-1]'] + 
                                      df['SPARE3 WHS (1-CT) [xpod chA-2]'] + 
                                      df['SPARE4 WHS (2-CTs) [xpod chA-5,6]'] + 
                                      df['Calculated Unmeasured loads (Whr)'])
    
    # Total: Total Building Load
    df['Total'] = df['TOTAL BLDG WHS [emon ch1,2]']
    
    # Group by season and hour, sum the components
    agg_df = df.groupby(['season', 'hour']).agg(
        HVAC=('HVAC', 'sum'),
        domestic_water_heating=('domestic_water_heating', 'sum'),
        major_appliances=('major_appliances', 'sum'),
        lighting=('lighting', 'sum'),
        miscellaneous_plug_loads=('miscellaneous_plug_loads', 'sum'),
        Total=('Total', 'sum')
    ).reset_index()
    
    # Ensure types match target
    # HVAC, DHW, Major, Lighting, Total are int64 in target
    # Misc is float64
    agg_df['HVAC'] = agg_df['HVAC'].astype('int64')
    agg_df['domestic_water_heating'] = agg_df['domestic_water_heating'].astype('int64')
    agg_df['major_appliances'] = agg_df['major_appliances'].astype('int64')
    agg_df['lighting'] = agg_df['lighting'].astype('int64')
    agg_df['Total'] = agg_df['Total'].astype('int64')
    # miscellaneous_plug_loads remains float64
    
    # Select and order columns
    result = agg_df[['season', 'hour', 'HVAC', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'Total']]
    
    return result
