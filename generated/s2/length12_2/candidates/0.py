import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    source = source.copy()
    source['dt'] = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    source['hour'] = source['dt'].dt.hour
    source['month'] = source['dt'].dt.month
    
    # Define season
    def get_season(m):
        if m in [12, 1, 2]:
            return 'Winter'
        elif m in [3, 4, 5]:
            return 'Spring'
        elif m in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
    
    source['season'] = source['month'].apply(get_season)
    
    # Define column mappings
    hvac_cols = ['air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum', 'furnace1_sum', 'furnace2_sum', 'heater1_sum', 'heater2_sum', 'heater3_sum', 'housefan1_sum']
    water_heating_cols = ['waterheater1_sum', 'waterheater2_sum']
    refrigerator_cols = ['refrigerator1_sum', 'refrigerator2_sum', 'winecooler1_sum', 'freezer1_sum', 'icemaker1_sum']
    clothes_washer_cols = ['clotheswasher1_sum']
    clothes_dryer_cols = ['drye1_sum', 'dryg1_sum', 'clotheswasher_dryg1_sum']
    dishwasher_cols = ['dishwasher1_sum']
    cooking_range_cols = ['oven1_sum', 'oven2_sum', 'range1_sum', 'microwave1_sum', 'disposal1_sum']
    pool_spa_pumps_cols = ['poolpump1_sum']
    pool_spa_heaters_cols = ['jacuzzi1_sum', 'pool1_sum', 'pool2_sum']
    interior_lighting_cols = ['lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum']
    exterior_lighting_cols = ['outsidelights_plugs1_sum', 'outsidelights_plugs2_sum', 'poollight1_sum']
    plug_cols = ['kitchenapp1_sum', 'kitchenapp2_sum', 'battery1_sum', 'security1_sum', 'venthood1_sum', 'pump1_sum', 'sumppump1_sum', 'sewerpump1_sum', 'wellpump1_sum', 'circpump1_sum', 'garage1_sum', 'garage2_sum', 'shed1_sum', 'car1_sum', 'car2_sum', 'aquarium1_sum', 'bathroom1_sum', 'bathroom2_sum', 'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum', 'diningroom1_sum', 'diningroom2_sum', 'kitchen1_sum', 'kitchen2_sum', 'livingroom1_sum', 'livingroom2_sum', 'office1_sum', 'utilityroom1_sum']
    
    # Calculate sums for each category
    source['hvac'] = source[hvac_cols].sum(axis=1)
    source['water_heating'] = source[water_heating_cols].sum(axis=1)
    source['refrigerator'] = source[refrigerator_cols].sum(axis=1)
    source['clothes_washer'] = source[clothes_washer_cols].sum(axis=1)
    source['clothes_dryer'] = source[clothes_dryer_cols].sum(axis=1)
    source['dishwasher'] = source[dishwasher_cols].sum(axis=1)
    source['cooking_range'] = source[cooking_range_cols].sum(axis=1)
    source['pool_spa_pumps'] = source[pool_spa_pumps_cols].sum(axis=1)
    source['pool_spa_heaters'] = source[pool_spa_heaters_cols].sum(axis=1)
    source['interior_lighting'] = source[interior_lighting_cols].sum(axis=1)
    source['exterior_lighting'] = source[exterior_lighting_cols].sum(axis=1)
    source['plug'] = source[plug_cols].sum(axis=1)
    
    # Aggregate by season and hour
    agg_cols = ['hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 'pool_spa_heaters', 'interior_lighting', 'exterior_lighting', 'plug']
    
    result = source.groupby(['season', 'hour'])[agg_cols].sum().reset_index()
    
    # Calculate lighting
    result['lighting'] = result['interior_lighting'] + result['exterior_lighting']
    
    # Reorder columns
    result = result[['season', 'hour', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heaters']]
    
    return result
