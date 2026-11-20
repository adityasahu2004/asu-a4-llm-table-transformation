import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    dt = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    hour = dt.dt.hour
    month = dt.dt.month
    
    # Define seasons
    def get_season(m):
        if m in [12, 1, 2]:
            return 'Winter'
        elif m in [3, 4, 5]:
            return 'Spring'
        elif m in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
            
    season = month.apply(get_season)
    
    # Define column groups
    # HVAC
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum', 'housefan1_sum', 'jacuzzi1_sum',
        'poolpump1_sum', 'sprinkler1_sum', 'sewerpump1_sum', 'sumppump1_sum',
        'circpump1_sum', 'heater1_sum', 'heater2_sum', 'heater3_sum', 'venthood1_sum'
    ]
    
    # Domestic Water Heating
    dwh_cols = [
        'waterheater1_sum', 'waterheater2_sum'
    ]
    
    # Major Appliances
    major_appl_cols = [
        'clotheswasher1_sum', 'dishwasher1_sum', 'drye1_sum', 'dryg1_sum',
        'microwave1_sum', 'oven1_sum', 'oven2_sum', 'range1_sum',
        'refrigerator1_sum', 'refrigerator2_sum', 'disposal1_sum', 
        'icemaker1_sum', 'clotheswasher_dryg1_sum'
    ]
    
    # Lighting
    lighting_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
        'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum',
        'poollight1_sum', 'security1_sum'
    ]
    
    # Miscellaneous Plug Loads
    misc_plug_cols = [
        'kitchenapp1_sum', 'kitchenapp2_sum', 'office1_sum',
        'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
        'garage1_sum', 'garage2_sum', 'shed1_sum', 'utilityroom1_sum',
        'livingroom1_sum', 'livingroom2_sum', 'diningroom1_sum', 'diningroom2_sum',
        'bathroom1_sum', 'bathroom2_sum', 'kitchen1_sum', 'kitchen2_sum',
        'aquarium1_sum', 'winecooler1_sum', 'battery1_sum', 'car1_sum', 'car2_sum'
    ]
    
    # Create a dataframe with the necessary columns
    df = pd.DataFrame()
    df['season'] = season
    df['hour'] = hour
    
    # Helper to sum columns safely
    def safe_sum(cols):
        # Select columns that exist in source
        existing_cols = [c for c in cols if c in source.columns]
        if not existing_cols:
            return pd.Series(0.0, index=df.index)
        # Sum across columns, treating NaN as 0
        return source[existing_cols].sum(axis=1, min_count=0).fillna(0)

    df['hvac'] = safe_sum(hvac_cols)
    df['domestic_water_heating'] = safe_sum(dwh_cols)
    df['major_appliances'] = safe_sum(major_appl_cols)
    df['lighting'] = safe_sum(lighting_cols)
    df['miscellaneous_plug_loads'] = safe_sum(misc_plug_cols)
    
    # Calculate total
    df['total'] = (df['hvac'] + df['domestic_water_heating'] + 
                   df['major_appliances'] + df['lighting'] + 
                   df['miscellaneous_plug_loads'])
    
    # Group by season and hour and sum the values
    result = df.groupby(['season', 'hour'], as_index=False).sum()
    
    # Ensure correct column order
    result = result[['season', 'hour', 'hvac', 'domestic_water_heating', 
                     'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    return result

transform
