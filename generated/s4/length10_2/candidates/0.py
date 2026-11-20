import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    dt = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    
    out = pd.DataFrame(index=source.index)
    out['datetime'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Define column mappings for summation
    hvac_cols = ['air1_sum', 'air2_sum', 'air3_sum', 'furnace1_sum', 'furnace2_sum', 
                 'heater1_sum', 'heater2_sum', 'heater3_sum', 'housefan1_sum', 'venthood1_sum']
    
    water_heating_cols = ['waterheater1_sum', 'waterheater2_sum', 'jacuzzi1_sum']
    
    refrigerator_cols = ['refrigerator1_sum', 'refrigerator2_sum', 'freezer1_sum', 
                         'icemaker1_sum', 'winecooler1_sum']
    
    clothes_washer_cols = ['clotheswasher1_sum']
    
    clothes_dryer_cols = ['drye1_sum', 'dryg1_sum', 'clotheswasher_dryg1_sum']
    
    dishwasher_cols = ['dishwasher1_sum']
    
    cooking_range_cols = ['oven1_sum', 'oven2_sum', 'range1_sum', 'microwave1_sum', 'disposal1_sum']
    
    pool_spa_pumps_cols = ['poolpump1_sum', 'circpump1_sum', 'pump1_sum', 'sumppump1_sum', 
                           'wellpump1_sum', 'sewerpump1_sum']
    
    interior_lighting_cols = ['lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 
                              'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
                              'livingroom1_sum', 'livingroom2_sum',
                              'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
                              'bathroom1_sum', 'bathroom2_sum',
                              'kitchen1_sum', 'kitchen2_sum',
                              'diningroom1_sum', 'diningroom2_sum',
                              'office1_sum', 'utilityroom1_sum',
                              'garage1_sum', 'garage2_sum', 'shed1_sum']
    
    exterior_lighting_cols = ['outsidelights_plugs1_sum', 'outsidelights_plugs2_sum', 'poollight1_sum']
    
    plug_cols = ['kitchenapp1_sum', 'kitchenapp2_sum', 'security1_sum', 'sprinkler1_sum',
                 'car1_sum', 'car2_sum', 'battery1_sum', 'aquarium1_sum']

    # Calculate sums
    out['hvac'] = source[hvac_cols].sum(axis=1)
    out['water_heating'] = source[water_heating_cols].sum(axis=1)
    out['refrigerator'] = source[refrigerator_cols].sum(axis=1)
    out['clothes_washer'] = source[clothes_washer_cols].sum(axis=1)
    out['clothes_dryer'] = source[clothes_dryer_cols].sum(axis=1)
    out['dishwasher'] = source[dishwasher_cols].sum(axis=1)
    out['cooking_range'] = source[cooking_range_cols].sum(axis=1)
    out['pool_spa_pumps'] = source[pool_spa_pumps_cols].sum(axis=1)
    out['interior_lighting'] = source[interior_lighting_cols].sum(axis=1)
    out['exterior_lighting'] = source[exterior_lighting_cols].sum(axis=1)
    out['lighting'] = out['interior_lighting'] + out['exterior_lighting']
    out['plug'] = source[plug_cols].sum(axis=1)
    out['pool_spa_heater'] = 0
    
    return out.reset_index(drop=True)
