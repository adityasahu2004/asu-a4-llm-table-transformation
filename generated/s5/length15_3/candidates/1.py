import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Parse timestamp
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
    
    # Replace 32767.0 with NaN
    cols_to_clean = [
        'TOTAL BLDG WHS [emon ch1,2]',
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'WATER HEATER WHS [emon ch7,8]',
        'DRYER WHS (1-CT) [emon ch9]',
        'RANGE WHS (1-CT) [emon ch10]',
        'DISH WASHER WHS [emon ch11]',
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]',
        'Calculated Unmeasured loads (Whr)'
    ]
    
    df[cols_to_clean] = df[cols_to_clean].replace(32767.0, np.nan)
    
    # Define components
    # HVAC: AC Compressor + Air Handler + Minisplit
    df['HVAC'] = (df['AC COMPRESSOR WHS [emon ch3,4]'] + 
                  df['AIR HANDLER WHS [emon ch5,6]'] + 
                  df['Minisplit WHS (2-CTs) [xpod chA-7,8]'])
    
    # Domestic Water Heating
    df['domestic_water_heating'] = df['WATER HEATER WHS [emon ch7,8]']
    
    # Major Appliances: Dryer(1-CT) + Range + Dishwasher + Fridge1 + Fridge2 + Dryer(2-CTs)
    df['major_appliances'] = (df['DRYER WHS (1-CT) [emon ch9]'] + 
                              df['RANGE WHS (1-CT) [emon ch10]'] + 
                              df['DISH WASHER WHS [emon ch11]'] + 
                              df['Primary Fridge WHS [emon ch12]'] + 
                              df['2nd Fridge WHS [emon ch13]'] + 
                              df['Dryer WHS (2-CTs) [xpod chA-9,10]'])
    
    # Lighting: 0
    df['lighting'] = 0
    
    # Miscellaneous Plug Loads: Calculated Unmeasured loads
    df['miscellaneous_plug_loads'] = df['Calculated Unmeasured loads (Whr)']
    
    # Total: TOTAL BLDG WHS
    df['Total'] = df['TOTAL BLDG WHS [emon ch1,2]']
    
    # Group by season and hour, sum the values
    agg_df = df.groupby(['season', 'hour']).agg({
        'HVAC': 'sum',
        'domestic_water_heating': 'sum',
        'major_appliances': 'sum',
        'lighting': 'sum',
        'miscellaneous_plug_loads': 'sum',
        'Total': 'sum'
    }).reset_index()
    
    # Ensure correct dtypes
    # HVAC, domestic_water_heating, major_appliances, lighting, Total -> int64
    # miscellaneous_plug_loads -> float64
    
    agg_df['HVAC'] = agg_df['HVAC'].astype(int)
    agg_df['domestic_water_heating'] = agg_df['domestic_water_heating'].astype(int)
    agg_df['major_appliances'] = agg_df['major_appliances'].astype(int)
    agg_df['lighting'] = agg_df['lighting'].astype(int)
    agg_df['miscellaneous_plug_loads'] = agg_df['miscellaneous_plug_loads'].astype(float)
    agg_df['Total'] = agg_df['Total'].astype(int)
    
    # Reorder columns to match target
    result = agg_df[['season', 'hour', 'HVAC', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'Total']]
    
    return result
