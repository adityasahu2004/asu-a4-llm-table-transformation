import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    dt = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    out = pd.DataFrame(index=source.index)
    out['month'] = dt.dt.month
    out['hour'] = dt.dt.hour

    # Define column groups
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum',
        'heater1_sum', 'heater2_sum', 'heater3_sum',
        'housefan1_sum'
    ]
    
    water_heating_cols = [
        'waterheater1_sum', 'waterheater2_sum'
    ]
    
    refrigerator_cols = [
        'refrigerator1_sum', 'refrigerator2_sum',
        'winecooler1_sum', 'icemaker1_sum'
    ]
    
    clothes_washer_cols = [
        'clotheswasher1_sum'
    ]
    
    clothes_dryer_cols = [
        'drye1_sum', 'dryg1_sum', 'clotheswasher_dryg1_sum'
    ]
    
    dishwasher_cols = [
        'dishwasher1_sum'
    ]
    
    cooking_range_cols = [
        'oven1_sum', 'oven2_sum', 'range1_sum',
        'microwave1_sum', 'disposal1_sum'
    ]
    
    pool_spa_pumps_cols = [
        'poolpump1_sum', 'circpump1_sum',
        'sumppump1_sum', 'sewerpump1_sum',
        'wellpump1_sum', 'pump1_sum'
    ]
    
    pool_spa_heater_cols = [
        'jacuzzi1_sum', 'pool1_sum'
    ]
    
    interior_lighting_cols = [
        'livingroom1_sum', 'livingroom2_sum',
        'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
        'bathroom1_sum', 'bathroom2_sum',
        'kitchen1_sum', 'kitchen2_sum',
        'office1_sum',
        'diningroom1_sum', 'diningroom2_sum',
        'utilityroom1_sum',
        'garage1_sum', 'garage2_sum',
        'shed1_sum', 'security1_sum',
        'aquarium1_sum'
    ]
    
    exterior_lighting_cols = [
        'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum',
        'poollight1_sum'
    ]
    
    plug_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum',
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
        'battery1_sum', 'car1_sum', 'car2_sum', 'sprinkler1_sum'
    ]

    # Helper to sum columns, handling NaNs properly
    # If all values in a row for the group are NaN, result is NaN.
    # If some are NaN, sum the non-NaN ones.
    def sum_group(cols):
        # Select columns, ensure float
        sub = source[cols].astype(float)
        # Sum across columns, skipping NaNs
        return sub.sum(axis=1)

    out['hvac'] = sum_group(hvac_cols)
    out['water_heating'] = sum_group(water_heating_cols)
    out['refrigerator'] = sum_group(refrigerator_cols)
    out['clothes_washer'] = sum_group(clothes_washer_cols)
    out['clothes_dryer'] = sum_group(clothes_dryer_cols)
    out['dishwasher'] = sum_group(dishwasher_cols)
    out['cooking_range'] = sum_group(cooking_range_cols)
    out['pool_spa_pumps'] = sum_group(pool_spa_pumps_cols)
    out['interior_lighting'] = sum_group(interior_lighting_cols)
    out['exterior_lighting'] = sum_group(exterior_lighting_cols)
    out['lighting'] = out['interior_lighting'] + out['exterior_lighting']
    out['plug'] = sum_group(plug_cols)
    out['pool_spa_heater'] = sum_group(pool_spa_heater_cols)

    return out.reset_index(drop=True)
