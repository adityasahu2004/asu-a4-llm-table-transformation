import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    dt = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    
    # Derive hour and season
    hour = dt.dt.hour
    month = dt.dt.month
    
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
    
    # Define columns for each category
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum',
        'heater1_sum', 'heater2_sum', 'heater3_sum',
        'housefan1_sum'
    ]
    
    dwh_cols = [
        'waterheater1_sum', 'waterheater2_sum'
    ]
    
    major_appl_cols = [
        'clotheswasher1_sum', 'clotheswasher_dryg1_sum',
        'dishwasher1_sum', 'drye1_sum', 'dryg1_sum',
        'oven1_sum', 'oven2_sum',
        'refrigerator1_sum', 'refrigerator2_sum',
        'microwave1_sum', 'freezer1_sum', 'icemaker1_sum',
        'winecooler1_sum', 'disposal1_sum', 'range1_sum'
    ]
    
    lighting_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum',
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
        'poollight1_sum', 'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum'
    ]
    
    misc_plug_cols = [
        'kitchen1_sum', 'kitchen2_sum', 'kitchenapp1_sum', 'kitchenapp2_sum',
        'livingroom1_sum', 'livingroom2_sum',
        'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
        'bathroom1_sum', 'bathroom2_sum',
        'office1_sum',
        'garage1_sum', 'garage2_sum',
        'utilityroom1_sum',
        'diningroom1_sum', 'diningroom2_sum',
        'shed1_sum', 'aquarium1_sum',
        'car1_sum', 'car2_sum',
        'circpump1_sum', 'security1_sum', 'sewerpump1_sum', 'sumppump1_sum',
        'venthood1_sum', 'wellpump1_sum', 'battery1_sum',
        'pool1_sum', 'pool2_sum', 'poolpump1_sum',
        'jacuzzi1_sum', 'sprinkler1_sum', 'pump1_sum'
    ]
    
    # Create a temporary dataframe with the derived keys and the sum columns
    # We fill NaNs with 0 for summing purposes
    temp = source[hvac_cols + dwh_cols + major_appl_cols + lighting_cols + misc_plug_cols].copy()
    temp = temp.fillna(0)
    
    temp['season'] = season
    temp['hour'] = hour
    
    # Group and sum
    grouped = temp.groupby(['season', 'hour'])
    
    hvac = grouped[hvac_cols].sum().sum(axis=1)
    dwh = grouped[dwh_cols].sum().sum(axis=1)
    major = grouped[major_appl_cols].sum().sum(axis=1)
    light = grouped[lighting_cols].sum().sum(axis=1)
    misc = grouped[misc_plug_cols].sum().sum(axis=1)
    
    # Construct result
    result = pd.DataFrame({
        'season': hvac.index.get_level_values('season'),
        'hour': hvac.index.get_level_values('hour'),
        'hvac': hvac.values,
        'domestic_water_heating': dwh.values,
        'major_appliances': major.values,
        'lighting': light.values,
        'miscellaneous_plug_loads': misc.values
    })
    
    result['total'] = result['hvac'] + result['domestic_water_heating'] + \
                      result['major_appliances'] + result['lighting'] + \
                      result['miscellaneous_plug_loads']
    
    # Ensure integer hour
    result['hour'] = result['hour'].astype(int)
    
    # Sort for consistency, though not strictly required by schema
    # The sample is not sorted, but let's return as is from groupby
    
    return result[['season', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
