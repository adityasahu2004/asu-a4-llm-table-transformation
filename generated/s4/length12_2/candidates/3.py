import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    source['dt'] = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    source['hour'] = source['dt'].dt.hour
    source['month'] = source['dt'].dt.month
    
    # Determine Season
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
    
    # Define column mappings for aggregation
    # We will sum these columns for each season/hour group
    
    hvac_cols = ['air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum', 
                 'furnace1_sum', 'furnace2_sum', 'heater1_sum', 'heater2_sum', 
                 'heater3_sum', 'housefan1_sum']
                 
    water_heating_cols = ['waterheater1_sum', 'waterheater2_sum', 'circpump1_sum']
    
    refrigerator_cols = ['refrigerator1_sum', 'refrigerator2_sum']
    
    clothes_washer_cols = ['clotheswasher1_sum']
    
    clothes_dryer_cols = ['drye1_sum', 'dryg1_sum']
    
    dishwasher_cols = ['dishwasher1_sum']
    
    cooking_range_cols = ['oven1_sum', 'oven2_sum', 'range1_sum', 'microwave1_sum']
    
    pool_spa_pumps_cols = ['poolpump1_sum', 'pool1_sum']
    
    interior_lighting_cols = ['kitchen1_sum', 'kitchen2_sum', 'diningroom1_sum', 
                              'livingroom1_sum', 'livingroom2_sum', 
                              'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 
                              'bedroom4_sum', 'bedroom5_sum', 
                              'bathroom1_sum', 'bathroom2_sum', 
                              'office1_sum', 'utilityroom1_sum', 
                              'garage1_sum', 'shed1_sum']
    
    exterior_lighting_cols = ['outsidelights_plugs1_sum', 'outsidelights_plugs2_sum', 'poollight1_sum']
    
    plug_cols = ['lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 
                 'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum', 
                 'kitchenapp1_sum', 'kitchenapp2_sum', 
                 'battery1_sum', 'car1_sum', 'car2_sum', 
                 'aquarium1_sum', 'winecooler1_sum', 'icemaker1_sum', 
                 'security1_sum', 'disposal1_sum', 'venthood1_sum', 
                 'garage2_sum', 'sumppump1_sum', 'wellpump1_sum', 'sewerpump1_sum',
                 'sprinkler1_sum', 'pump1_sum']
                 
    pool_spa_heaters_cols = ['jacuzzi1_sum', 'pool2_sum']

    # Group by season and hour and sum
    grouped = source.groupby(['season', 'hour'])
    
    agg_data = {}
    
    # Helper to sum columns, filling NaN with 0 for sum
    def sum_cols(cols):
        # Select columns that exist in source
        existing_cols = [c for c in cols if c in source.columns]
        if not existing_cols:
            return pd.Series(0, index=grouped.groups.keys())
        # Sum across columns for each group
        # We need to sum the values in each group for these columns
        # groupby.sum() sums the rows within the group.
        # We want the sum of multiple columns within that group.
        # So we can sum the sub-dataframe
        return grouped[existing_cols].sum().sum(axis=1)

    # Generate sums for each category
    hvac = sum_cols(hvac_cols)
    water_heating = sum_cols(water_heating_cols)
    refrigerator = sum_cols(refrigerator_cols)
    clothes_washer = sum_cols(clothes_washer_cols)
    clothes_dryer = sum_cols(clothes_dryer_cols)
    dishwasher = sum_cols(dishwasher_cols)
    cooking_range = sum_cols(cooking_range_cols)
    pool_spa_pumps = sum_cols(pool_spa_pumps_cols)
    interior_lighting = sum_cols(interior_lighting_cols)
    exterior_lighting = sum_cols(exterior_lighting_cols)
    plug = sum_cols(plug_cols)
    pool_spa_heaters = sum_cols(pool_spa_heaters_cols)
    
    # Create result DataFrame
    # The index of the summed series is (season, hour)
    result = pd.DataFrame(index=hvac.index)
    result.index.names = ['season', 'hour']
    
    result['season'] = result.index.get_level_values('season')
    result['hour'] = result.index.get_level_values('hour')
    
    result['hvac'] = hvac.values
    result['water_heating'] = water_heating.values
    result['refrigerator'] = refrigerator.values
    result['clothes_washer'] = clothes_washer.values
    result['clothes_dryer'] = clothes_dryer.values
    result['dishwasher'] = dishwasher.values
    result['cooking_range'] = cooking_range.values
    result['pool_spa_pumps'] = pool_spa_pumps.values
    result['interior_lighting'] = interior_lighting.values
    result['exterior_lighting'] = exterior_lighting.values
    result['lighting'] = interior_lighting.values + exterior_lighting.values
    result['plug'] = plug.values
    result['pool_spa_heaters'] = pool_spa_heaters.values
    
    # Reset index to make season and hour regular columns
    result = result.reset_index(drop=True)
    
    # Ensure correct column order
    cols = ['season', 'hour', 'hvac', 'water_heating', 'refrigerator', 
            'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 
            'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
            'lighting', 'plug', 'pool_spa_heaters']
            
    result = result[cols]
    
    return result
