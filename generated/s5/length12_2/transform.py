import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    df = source.copy()
    df['dt'] = pd.to_datetime(df['local_15min'])
    
    # Derive Season
    month = df['dt'].dt.month
    def get_season(m):
        if m in [12, 1, 2]:
            return 'Winter'
        elif m in [3, 4, 5]:
            return 'Spring'
        elif m in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
            
    df['season'] = month.apply(get_season)
    df['hour'] = df['dt'].dt.hour
    
    # Define column mappings
    hvac_cols = ['air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum', 
                 'furnace1_sum', 'furnace2_sum', 'heater1_sum', 'heater2_sum', 'heater3_sum']
    
    water_heating_cols = ['waterheater1_sum', 'waterheater2_sum']
    
    refrigerator_cols = ['refrigerator1_sum', 'refrigerator2_sum']
    
    clothes_washer_cols = ['clotheswasher1_sum']
    
    clothes_dryer_cols = ['drye1_sum', 'dryg1_sum']
    
    dishwasher_cols = ['dishwasher1_sum']
    
    cooking_range_cols = ['oven1_sum', 'oven2_sum', 'range1_sum', 'microwave1_sum']
    
    pool_spa_pumps_cols = ['poolpump1_sum', 'jacuzzi1_sum']
    
    interior_lighting_cols = ['bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
                              'bathroom1_sum', 'bathroom2_sum', 'kitchen1_sum', 'kitchen2_sum',
                              'livingroom1_sum', 'livingroom2_sum', 'diningroom1_sum', 'diningroom2_sum',
                              'office1_sum', 'utilityroom1_sum', 'shed1_sum']
    
    exterior_lighting_cols = ['outsidelights_plugs1_sum', 'outsidelights_plugs2_sum', 
                              'garage1_sum', 'garage2_sum', 'poollight1_sum']
    
    plug_cols = ['kitchenapp1_sum', 'kitchenapp2_sum', 
                 'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 
                 'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
                 'disposal1_sum', 'icemaker1_sum', 'aquarium1_sum', 'security1_sum', 
                 'battery1_sum', 'winecooler1_sum', 'venthood1_sum']
                 
    pool_spa_heaters_cols = ['pool1_sum', 'pool2_sum']

    # Create aggregated columns, filling NaNs with 0 for summing purposes
    def safe_sum(cols):
        return df[cols].fillna(0).sum(axis=1)

    df['hvac'] = safe_sum(hvac_cols)
    df['water_heating'] = safe_sum(water_heating_cols)
    df['refrigerator'] = safe_sum(refrigerator_cols)
    df['clothes_washer'] = safe_sum(clothes_washer_cols)
    df['clothes_dryer'] = safe_sum(clothes_dryer_cols)
    df['dishwasher'] = safe_sum(dishwasher_cols)
    df['cooking_range'] = safe_sum(cooking_range_cols)
    df['pool_spa_pumps'] = safe_sum(pool_spa_pumps_cols)
    df['interior_lighting'] = safe_sum(interior_lighting_cols)
    df['exterior_lighting'] = safe_sum(exterior_lighting_cols)
    df['plug'] = safe_sum(plug_cols)
    df['pool_spa_heaters'] = safe_sum(pool_spa_heaters_cols)
    
    # Lighting is sum of interior and exterior
    df['lighting'] = df['interior_lighting'] + df['exterior_lighting']
    
    # Group by season and hour, sum the values
    target_cols = [
        'season', 'hour', 
        'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer', 
        'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 
        'exterior_lighting', 'lighting', 'plug', 'pool_spa_heaters'
    ]
    
    agg_df = df.groupby(['season', 'hour'])[target_cols[2:]].sum().reset_index()
    
    return agg_df[['season', 'hour', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heaters']]
