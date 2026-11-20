import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    dt = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    out = pd.DataFrame()
    out['datetime'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Define groups
    hvac_cols = ['air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum', 
                 'heater1_sum', 'heater2_sum', 'heater3_sum', 
                 'furnace1_sum', 'furnace2_sum']
    
    water_heating_cols = ['waterheater1_sum', 'waterheater2_sum']
    
    refrigerator_cols = ['refrigerator1_sum', 'refrigerator2_sum', 
                         'winecooler1_sum', 'icemaker1_sum', 'freezer1_sum']
    
    clothes_washer_cols = ['clotheswasher1_sum']
    
    clothes_dryer_cols = ['clotheswasher_dryg1_sum', 'drye1_sum', 'dryg1_sum']
    
    dishwasher_cols = ['dishwasher1_sum']
    
    cooking_range_cols = ['oven1_sum', 'oven2_sum', 'range1_sum', 
                          'microwave1_sum', 'disposal1_sum']
    
    pool_spa_pumps_cols = ['poolpump1_sum', 'pool1_sum', 'pool2_sum', 
                           'sumppump1_sum', 'sewerpump1_sum', 'wellpump1_sum', 
                           'circpump1_sum', 'pump1_sum']
    
    interior_lighting_cols = ['kitchen1_sum', 'kitchen2_sum', 'diningroom1_sum', 
                              'livingroom1_sum', 'livingroom2_sum', 
                              'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 
                              'bedroom4_sum', 'bedroom5_sum', 
                              'bathroom1_sum', 'bathroom2_sum', 
                              'office1_sum', 'utilityroom1_sum', 
                              'garage1_sum', 'garage2_sum', 'shed1_sum', 
                              'housefan1_sum', 'venthood1_sum', 
                              'kitchenapp1_sum', 'kitchenapp2_sum']
    
    exterior_lighting_cols = ['outsidelights_plugs1_sum', 'outsidelights_plugs2_sum', 
                              'sprinkler1_sum']
    
    plug_cols = ['lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 
                 'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum', 
                 'car1_sum', 'car2_sum', 'battery1_sum', 'aquarium1_sum', 
                 'security1_sum', 'solar2_sum']

    # Helper to sum columns
    def sum_cols(cols):
        return source[cols].sum(axis=1, skipna=True)

    out['hvac'] = sum_cols(hvac_cols)
    out['water_heating'] = sum_cols(water_heating_cols)
    out['refrigerator'] = sum_cols(refrigerator_cols)
    out['clothes_washer'] = sum_cols(clothes_washer_cols)
    out['clothes_dryer'] = sum_cols(clothes_dryer_cols)
    out['dishwasher'] = sum_cols(dishwasher_cols)
    out['cooking_range'] = sum_cols(cooking_range_cols)
    out['pool_spa_pumps'] = sum_cols(pool_spa_pumps_cols)
    out['interior_lighting'] = sum_cols(interior_lighting_cols)
    out['exterior_lighting'] = sum_cols(exterior_lighting_cols)
    out['lighting'] = out['interior_lighting'] + out['exterior_lighting']
    out['plug'] = sum_cols(plug_cols)
    out['pool_spa_heater'] = 0
    
    return out.reset_index(drop=True)
