import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    dt = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    month = dt.dt.month.astype(int)
    hour = dt.dt.hour.astype(int)
    
    # Define column groups
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum', 'housefan1_sum',
        'sumppump1_sum', 'circpump1_sum'
    ]
    
    water_heating_cols = [
        'waterheater1_sum', 'waterheater2_sum'
    ]
    
    refrigerator_cols = [
        'refrigerator1_sum', 'refrigerator2_sum', 'freezer1_sum',
        'icemaker1_sum', 'winecooler1_sum'
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
        'oven1_sum', 'oven2_sum', 'range1_sum', 'microwave1_sum', 'disposal1_sum'
    ]
    
    pool_spa_pumps_cols = [
        'poolpump1_sum', 'sprinkler1_sum', 'pump1_sum'
    ]
    
    interior_lighting_cols = [
        'kitchen1_sum', 'kitchen2_sum',
        'livingroom1_sum', 'livingroom2_sum',
        'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
        'bathroom1_sum', 'bathroom2_sum',
        'diningroom1_sum', 'diningroom2_sum',
        'office1_sum',
        'garage1_sum', 'garage2_sum',
        'utilityroom1_sum', 'shed1_sum'
    ]
    
    exterior_lighting_cols = [
        'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum', 'poollight1_sum'
    ]
    
    plug_cols = [
        'kitchenapp1_sum', 'kitchenapp2_sum',
        'battery1_sum', 'security1_sum',
        'car1_sum', 'car2_sum',
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum',
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum'
    ]
    
    pool_spa_heater_cols = [
        'jacuzzi1_sum', 'pool1_sum', 'pool2_sum'
    ]

    # Helper to sum columns safely
    def sum_cols(cols):
        # Filter to existing columns in source to avoid KeyError if schema varies slightly
        valid_cols = [c for c in cols if c in source.columns]
        if not valid_cols:
            return pd.Series(np.nan, index=source.index)
        return source[valid_cols].sum(axis=1, min_count=1)

    out = pd.DataFrame()
    out['month'] = month
    out['hour'] = hour
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
    out['pool_spa_heater'] = sum_cols(pool_spa_heater_cols)
    
    return out.reset_index(drop=True)
