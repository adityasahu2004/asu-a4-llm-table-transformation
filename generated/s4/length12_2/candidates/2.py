import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    source['dt'] = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    
    # Derive Season and Hour
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
            
    source['season'] = source['dt'].dt.month.apply(get_season)
    source['hour'] = source['dt'].dt.hour
    
    # Define column mappings
    hvac_cols = ['air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum', 'furnace1_sum', 'furnace2_sum', 'heater1_sum', 'heater2_sum', 'heater3_sum', 'housefan1_sum']
    water_heating_cols = ['waterheater1_sum', 'waterheater2_sum']
    refrigerator_cols = ['refrigerator1_sum', 'refrigerator2_sum', 'freezer1_sum', 'winecooler1_sum', 'icemaker1_sum']
    clothes_washer_cols = ['clotheswasher1_sum']
    clothes_dryer_cols = ['drye1_sum', 'dryg1_sum', 'clotheswasher_dryg1_sum']
    dishwasher_cols = ['dishwasher1_sum']
    cooking_range_cols = ['oven1_sum', 'oven2_sum', 'range1_sum', 'microwave1_sum', 'disposal1_sum']
    pool_spa_pumps_cols = ['poolpump1_sum', 'jacuzzi1_sum', 'pump1_sum', 'circpump1_sum', 'sumppump1_sum', 'sewerpump1_sum', 'wellpump1_sum']
    interior_lighting_cols = ['lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum']
    exterior_lighting_cols = ['outsidelights_plugs1_sum', 'outsidelights_plugs2_sum', 'poollight1_sum', 'security1_sum', 'garage1_sum', 'garage2_sum', 'shed1_sum']
    plug_cols = ['kitchenapp1_sum', 'kitchenapp2_sum', 'battery1_sum', 'car1_sum', 'car2_sum', 'aquarium1_sum', 'bathroom1_sum', 'bathroom2_sum', 'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum', 'livingroom1_sum', 'livingroom2_sum', 'office1_sum', 'utilityroom1_sum', 'diningroom1_sum', 'diningroom2_sum', 'kitchen1_sum', 'kitchen2_sum']
    pool_spa_heaters_cols = ['pool1_sum', 'pool2_sum']

    # Group by season and hour
    grouped = source.groupby(['season', 'hour'])
    
    # Aggregate sums
    result = grouped.sum(numeric_only=True)
    
    # Create target columns
    out = pd.DataFrame()
    out['season'] = result.index.get_level_values('season')
    out['hour'] = result.index.get_level_values('hour')
    
    out['hvac'] = result[hvac_cols].sum(axis=1)
    out['water_heating'] = result[water_heating_cols].sum(axis=1)
    out['refrigerator'] = result[refrigerator_cols].sum(axis=1)
    out['clothes_washer'] = result[clothes_washer_cols].sum(axis=1)
    out['clothes_dryer'] = result[clothes_dryer_cols].sum(axis=1)
    out['dishwasher'] = result[dishwasher_cols].sum(axis=1)
    out['cooking_range'] = result[cooking_range_cols].sum(axis=1)
    out['pool_spa_pumps'] = result[pool_spa_pumps_cols].sum(axis=1)
    out['interior_lighting'] = result[interior_lighting_cols].sum(axis=1)
    out['exterior_lighting'] = result[exterior_lighting_cols].sum(axis=1)
    out['lighting'] = out['interior_lighting'] + out['exterior_lighting']
    out['plug'] = result[plug_cols].sum(axis=1)
    out['pool_spa_heaters'] = result[pool_spa_heaters_cols].sum(axis=1)
    
    # Reset index to flatten
    out = out.reset_index(drop=True)
    
    return out
