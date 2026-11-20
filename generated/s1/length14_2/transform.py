import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse timestamp
    source = source.copy()
    source['local_15min'] = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    source['month'] = source['local_15min'].dt.month
    source['hour'] = source['local_15min'].dt.hour

    # 2. Define columns for each category
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum', 'heater1_sum', 'heater2_sum', 'heater3_sum',
        'housefan1_sum', 'venthood1_sum'
    ]
    
    dwh_cols = [
        'waterheater1_sum', 'waterheater2_sum'
    ]
    
    major_appliances_cols = [
        'clotheswasher1_sum', 'clotheswasher_dryg1_sum', 'dishwasher1_sum',
        'drye1_sum', 'dryg1_sum', 'microwave1_sum', 'oven1_sum', 'oven2_sum',
        'range1_sum', 'refrigerator1_sum', 'refrigerator2_sum', 'freezer1_sum',
        'icemaker1_sum', 'winecooler1_sum'
    ]
    
    lighting_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum',
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
        'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum', 'poollight1_sum'
    ]
    
    misc_cols = [
        'aquarium1_sum', 'battery1_sum', 'car1_sum', 'car2_sum', 'circpump1_sum',
        'disposal1_sum', 'jacuzzi1_sum', 'kitchen1_sum', 'kitchen2_sum',
        'kitchenapp1_sum', 'kitchenapp2_sum', 'livingroom1_sum', 'livingroom2_sum',
        'office1_sum', 'pool1_sum', 'pool2_sum', 'poolpump1_sum', 'pump1_sum',
        'security1_sum', 'sewerpump1_sum', 'shed1_sum', 'sprinkler1_sum',
        'sumppump1_sum', 'utilityroom1_sum', 'wellpump1_sum',
        'bathroom1_sum', 'bathroom2_sum', 'bedroom1_sum', 'bedroom2_sum',
        'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum', 'diningroom1_sum',
        'diningroom2_sum', 'garage1_sum', 'garage2_sum'
    ]

    # 3. Calculate sums for each category, treating NaN as 0
    source['hvac'] = source[hvac_cols].fillna(0).sum(axis=1)
    source['domestic_water_heating'] = source[dwh_cols].fillna(0).sum(axis=1)
    source['major_appliances'] = source[major_appliances_cols].fillna(0).sum(axis=1)
    source['lighting'] = source[lighting_cols].fillna(0).sum(axis=1)
    source['miscellaneous_plug_loads'] = source[misc_cols].fillna(0).sum(axis=1)
    
    # 4. Calculate total
    source['total'] = source['hvac'] + source['domestic_water_heating'] + \
                      source['major_appliances'] + source['lighting'] + \
                      source['miscellaneous_plug_loads']

    # 5. Group by month and hour and sum
    result = source.groupby(['month', 'hour'], as_index=False).agg({
        'hvac': 'sum',
        'domestic_water_heating': 'sum',
        'major_appliances': 'sum',
        'lighting': 'sum',
        'miscellaneous_plug_loads': 'sum',
        'total': 'sum'
    })

    # 6. Ensure correct column order and types
    result = result[['month', 'hour', 'hvac', 'domestic_water_heating', 
                     'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    # Ensure integer types for month and hour
    result['month'] = result['month'].astype('int64')
    result['hour'] = result['hour'].astype('int64')
    
    return result
