import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse time
    df = source.copy()
    df['time_dt'] = pd.to_datetime(df['time'])
    df['hour'] = df['time_dt'].dt.hour
    df['month'] = df['time_dt'].dt.month
    
    # Map month to season
    def get_season(m):
        if m in [12, 1, 2]:
            return 'Winter'
        elif m in [3, 4, 5]:
            return 'Spring'
        elif m in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
            
    df['season'] = df['month'].apply(get_season)
    
    # Define HVAC columns
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_central_system_heating_kwh',
        'electricity_central_system_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_central_system_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh',
        'electricity_central_system_pumps_cooling_kwh'
    ]
    
    # Calculate sums for grouped columns
    df['hvac'] = df[hvac_cols].sum(axis=1)
    df['pool_spa_pumps'] = df['electricity_pool_pump_kwh'] + df['electricity_hot_tub_pump_kwh']
    df['pool_spa_heaters'] = df['electricity_pool_heater_kwh'] + df['electricity_hot_tub_heater_kwh']
    df['lighting'] = df['electricity_interior_lighting_kwh'] + df['electricity_exterior_lighting_kwh']
    
    # Map source columns to target names
    agg_map = {
        'hvac': 'hvac',
        'electricity_water_systems_kwh': 'water_heating',
        'electricity_refrigerator_kwh': 'refrigerator',
        'electricity_clothes_washer_kwh': 'clothes_washer',
        'electricity_clothes_dryer_kwh': 'clothes_dryer',
        'electricity_dishwasher_kwh': 'dishwasher',
        'electricity_cooking_range_kwh': 'cooking_range',
        'pool_spa_pumps': 'pool_spa_pumps',
        'electricity_interior_lighting_kwh': 'interior_lighting',
        'electricity_exterior_lighting_kwh': 'exterior_lighting',
        'lighting': 'lighting',
        'electricity_plug_loads_kwh': 'plug',
        'pool_spa_heaters': 'pool_spa_heaters'
    }
    
    # Select columns to aggregate
    agg_cols = list(agg_map.keys())
    
    # Group and sum
    grouped = df.groupby(['season', 'hour'])[agg_cols].sum().reset_index()
    
    # Rename columns
    grouped = grouped.rename(columns=agg_map)
    
    # Select and order columns as per target
    target_cols = [
        'season', 'hour', 'hvac', 'water_heating', 'refrigerator', 
        'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 
        'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
        'lighting', 'plug', 'pool_spa_heaters'
    ]
    
    result = grouped[target_cols]
    
    # Ensure hour is int64
    result['hour'] = result['hour'].astype('int64')
    
    return result
