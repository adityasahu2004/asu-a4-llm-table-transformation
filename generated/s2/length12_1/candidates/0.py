import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse time
    source = source.copy()
    source['time_dt'] = pd.to_datetime(source['time'])
    source['hour'] = source['time_dt'].dt.hour
    source['month'] = source['time_dt'].dt.month
    
    # Map to Season
    # Assuming:
    # Summer: 6, 7, 8
    # Spring: 3, 4, 5
    # Winter: 12, 1, 2, 9, 10, 11 (Grouping Fall into Winter as 'Fall' is not in target distincts)
    def get_season(m):
        if m in [6, 7, 8]:
            return "Summer"
        elif m in [3, 4, 5]:
            return "Spring"
        else:
            return "Winter"
            
    source['season'] = source['month'].apply(get_season)
    
    # Define HVAC components
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_central_system_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh',
        'electricity_central_system_pumps_cooling_kwh'
    ]
    
    # Calculate derived columns for aggregation
    source['hvac'] = source[hvac_cols].sum(axis=1)
    source['water_heating'] = source['electricity_water_systems_kwh']
    source['refrigerator'] = source['electricity_refrigerator_kwh']
    source['clothes_washer'] = source['electricity_clothes_washer_kwh']
    source['clothes_dryer'] = source['electricity_clothes_dryer_kwh']
    source['dishwasher'] = source['electricity_dishwasher_kwh']
    source['cooking_range'] = source['electricity_cooking_range_kwh']
    source['pool_spa_pumps'] = source['electricity_pool_pump_kwh'] + source['electricity_hot_tub_pump_kwh']
    source['interior_lighting'] = source['electricity_interior_lighting_kwh']
    source['exterior_lighting'] = source['electricity_exterior_lighting_kwh']
    source['lighting'] = source['interior_lighting'] + source['exterior_lighting']
    source['plug'] = source['electricity_plug_loads_kwh']
    source['pool_spa_heaters'] = source['electricity_pool_heater_kwh'] + source['electricity_hot_tub_heater_kwh']
    
    # Aggregate
    agg_cols = [
        'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 
        'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps',
        'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 
        'pool_spa_heaters'
    ]
    
    result = source.groupby(['season', 'hour'])[agg_cols].sum().reset_index()
    
    # Ensure correct column order and types
    result = result[['season', 'hour', 'hvac', 'water_heating', 'refrigerator', 
                     'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 
                     'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
                     'lighting', 'plug', 'pool_spa_heaters']]
    
    return result
