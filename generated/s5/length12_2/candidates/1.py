import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    source = source.copy()
    source['dt'] = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    
    # Derive season
    month = source['dt'].dt.month
    season_map = {1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring', 5: 'Spring', 
                  6: 'Summer', 7: 'Summer', 8: 'Summer', 9: 'Fall', 10: 'Fall', 
                  11: 'Fall', 12: 'Winter'}
    source['season'] = month.map(season_map)
    source['hour'] = source['dt'].dt.hour
    
    # Define column mappings
    hvac_cols = ['air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum', 
                 'furnace1_sum', 'furnace2_sum', 'heater1_sum', 'heater2_sum', 
                 'heater3_sum', 'housefan1_sum', 'venthood1_sum', 'circpump1_sum']
    
    water_heating_cols = ['waterheater1_sum', 'waterheater2_sum']
    
    refrigerator_cols = ['refrigerator1_sum', 'refrigerator2_sum', 'icemaker1_sum', 'winecooler1_sum']
    
    clothes_washer_cols = ['clotheswasher1_sum', 'clotheswasher_dryg1_sum']
    
    clothes_dryer_cols = ['drye1_sum', 'dryg1_sum']
    
    dishwasher_cols = ['dishwasher1_sum', 'disposal1_sum']
    
    cooking_range_cols = ['oven1_sum', 'oven2_sum', 'range1_sum', 'microwave1_sum']
    
    pool_spa_pumps_cols = ['poolpump1_sum', 'pump1_sum', 'pool2_sum']
    
    pool_spa_heaters_cols = ['pool1_sum', 'jacuzzi1_sum']
    
    interior_lighting_cols = ['lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 
                              'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum']
    
    exterior_lighting_cols = ['outsidelights_plugs1_sum', 'outsidelights_plugs2_sum', 'poollight1_sum']
    
    plug_cols = ['kitchenapp1_sum', 'kitchenapp2_sum', 'livingroom1_sum', 'livingroom2_sum',
                 'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
                 'office1_sum', 'garage1_sum', 'garage2_sum', 'shed1_sum', 'security1_sum',
                 'car1_sum', 'car2_sum', 'battery1_sum', 'aquarium1_sum', 'bathroom1_sum', 
                 'bathroom2_sum', 'diningroom1_sum', 'diningroom2_sum', 'utilityroom1_sum']

    # Aggregate
    agg_dict = {}
    for col in hvac_cols:
        agg_dict[f'hvac_{col}'] = 'sum'
    for col in water_heating_cols:
        agg_dict[f'wh_{col}'] = 'sum'
    for col in refrigerator_cols:
        agg_dict[f'ref_{col}'] = 'sum'
    for col in clothes_washer_cols:
        agg_dict[f'cw_{col}'] = 'sum'
    for col in clothes_dryer_cols:
        agg_dict[f'cd_{col}'] = 'sum'
    for col in dishwasher_cols:
        agg_dict[f'dw_{col}'] = 'sum'
    for col in cooking_range_cols:
        agg_dict[f'cr_{col}'] = 'sum'
    for col in pool_spa_pumps_cols:
        agg_dict[f'psp_{col}'] = 'sum'
    for col in pool_spa_heaters_cols:
        agg_dict[f'pshe_{col}'] = 'sum'
    for col in interior_lighting_cols:
        agg_dict[f'il_{col}'] = 'sum'
    for col in exterior_lighting_cols:
        agg_dict[f'el_{col}'] = 'sum'
    for col in plug_cols:
        agg_dict[f'plug_{col}'] = 'sum'

    # Group by season and hour
    grouped = source.groupby(['season', 'hour']).agg(agg_dict).reset_index()
    
    # Sum up the categories
    out = pd.DataFrame()
    out['season'] = grouped['season']
    out['hour'] = grouped['hour']
    
    out['hvac'] = grouped[[f'hvac_{c}' for c in hvac_cols]].sum(axis=1)
    out['water_heating'] = grouped[[f'wh_{c}' for c in water_heating_cols]].sum(axis=1)
    out['refrigerator'] = grouped[[f'ref_{c}' for c in refrigerator_cols]].sum(axis=1)
    out['clothes_washer'] = grouped[[f'cw_{c}' for c in clothes_washer_cols]].sum(axis=1)
    out['clothes_dryer'] = grouped[[f'cd_{c}' for c in clothes_dryer_cols]].sum(axis=1)
    out['dishwasher'] = grouped[[f'dw_{c}' for c in dishwasher_cols]].sum(axis=1)
    out['cooking_range'] = grouped[[f'cr_{c}' for c in cooking_range_cols]].sum(axis=1)
    out['pool_spa_pumps'] = grouped[[f'psp_{c}' for c in pool_spa_pumps_cols]].sum(axis=1)
    out['interior_lighting'] = grouped[[f'il_{c}' for c in interior_lighting_cols]].sum(axis=1)
    out['exterior_lighting'] = grouped[[f'el_{c}' for c in exterior_lighting_cols]].sum(axis=1)
    out['plug'] = grouped[[f'plug_{c}' for c in plug_cols]].sum(axis=1)
    out['pool_spa_heaters'] = grouped[[f'pshe_{c}' for c in pool_spa_heaters_cols]].sum(axis=1)
    
    out['lighting'] = out['interior_lighting'] + out['exterior_lighting']
    
    # Select and order columns
    cols = ['season', 'hour', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 
            'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 
            'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heaters']
    
    return out[cols]
