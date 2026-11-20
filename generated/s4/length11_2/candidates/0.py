import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the timestamp
    source = source.copy()
    source['local_15min'] = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    source['month'] = source['local_15min'].dt.month
    source['hour'] = source['local_15min'].dt.hour
    
    # Define column mappings for aggregation
    hvac_cols = ['air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum', 
                 'furnace1_sum', 'furnace2_sum', 'heater1_sum', 'heater2_sum', 'heater3_sum',
                 'housefan1_sum', 'venthood1_sum']
    
    water_heating_cols = ['waterheater1_sum', 'waterheater2_sum']
    
    refrigerator_cols = ['refrigerator1_sum', 'refrigerator2_sum', 'freezer1_sum', 
                         'icemaker1_sum', 'winecooler1_sum']
    
    clothes_washer_cols = ['clotheswasher1_sum']
    
    clothes_dryer_cols = ['drye1_sum', 'dryg1_sum']
    
    dishwasher_cols = ['dishwasher1_sum']
    
    cooking_range_cols = ['oven1_sum', 'oven2_sum', 'range1_sum', 'microwave1_sum', 'disposal1_sum']
    
    pool_spa_pumps_cols = ['poolpump1_sum', 'pool1_sum', 'pool2_sum', 'sprinkler1_sum',
                           'sumppump1_sum', 'sewerpump1_sum', 'circpump1_sum']
    
    interior_lighting_cols = ['kitchen1_sum', 'kitchen2_sum', 'bathroom1_sum', 'bathroom2_sum',
                              'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
                              'diningroom1_sum', 'diningroom2_sum', 'livingroom1_sum', 'livingroom2_sum',
                              'office1_sum', 'garage1_sum', 'garage2_sum', 'shed1_sum', 'utilityroom1_sum']
    
    exterior_lighting_cols = ['outsidelights_plugs1_sum', 'outsidelights_plugs2_sum', 'poollight1_sum']
    
    plug_cols = ['kitchenapp1_sum', 'kitchenapp2_sum', 'lights_plugs1_sum', 'lights_plugs2_sum',
                 'lights_plugs3_sum', 'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
                 'car1_sum', 'car2_sum', 'battery1_sum', 'aquarium1_sum', 'security1_sum']
    
    pool_spa_heater_cols = ['jacuzzi1_sum']

    # Group by month and hour and sum the respective columns
    grouped = source.groupby(['month', 'hour'])
    
    def safe_sum(cols):
        if not cols:
            return pd.Series(dtype='float64')
        return grouped[cols].sum()

    hvac = safe_sum(hvac_cols)
    water_heating = safe_sum(water_heating_cols)
    refrigerator = safe_sum(refrigerator_cols)
    clothes_washer = safe_sum(clothes_washer_cols)
    clothes_dryer = safe_sum(clothes_dryer_cols)
    dishwasher = safe_sum(dishwasher_cols)
    cooking_range = safe_sum(cooking_range_cols)
    pool_spa_pumps = safe_sum(pool_spa_pumps_cols)
    interior_lighting = safe_sum(interior_lighting_cols)
    exterior_lighting = safe_sum(exterior_lighting_cols)
    plug = safe_sum(plug_cols)
    pool_spa_heater = safe_sum(pool_spa_heater_cols)
    
    # Combine into a DataFrame
    result = pd.DataFrame({
        'hvac': hvac.values if isinstance(hvac, pd.Series) else hvac,
        'water_heating': water_heating.values if isinstance(water_heating, pd.Series) else water_heating,
        'refrigerator': refrigerator.values if isinstance(refrigerator, pd.Series) else refrigerator,
        'clothes_washer': clothes_washer.values if isinstance(clothes_washer, pd.Series) else clothes_washer,
        'clothes_dryer': clothes_dryer.values if isinstance(clothes_dryer, pd.Series) else clothes_dryer,
        'dishwasher': dishwasher.values if isinstance(dishwasher, pd.Series) else dishwasher,
        'cooking_range': cooking_range.values if isinstance(cooking_range, pd.Series) else cooking_range,
        'pool_spa_pumps': pool_spa_pumps.values if isinstance(pool_spa_pumps, pd.Series) else pool_spa_pumps,
        'interior_lighting': interior_lighting.values if isinstance(interior_lighting, pd.Series) else interior_lighting,
        'exterior_lighting': exterior_lighting.values if isinstance(exterior_lighting, pd.Series) else exterior_lighting,
        'plug': plug.values if isinstance(plug, pd.Series) else plug,
        'pool_spa_heater': pool_spa_heater.values if isinstance(pool_spa_heater, pd.Series) else pool_spa_heater
    })
    
    # Calculate total lighting
    result['lighting'] = result['interior_lighting'] + result['exterior_lighting']
    
    # Ensure correct column order
    cols = ['month', 'hour', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 
            'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 
            'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    
    return result[cols].reset_index()
