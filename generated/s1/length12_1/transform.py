import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse time
    df = source.copy()
    df['time'] = pd.to_datetime(df['time'])
    
    # 2. Extract hour and month
    df['hour'] = df['time'].dt.hour
    df['month'] = df['time'].dt.month
    
    # 3. Determine season and filter
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Autumn' # Will be filtered out
            
    df['season'] = df['month'].apply(get_season)
    
    # Filter out Autumn as it's not in the target distinct values
    df = df[df['season'] != 'Autumn'].reset_index(drop=True)
    
    # 4. Define aggregation columns
    # HVAC: heating + cooling
    df['hvac'] = df['electricity_heating_kwh'] + df['electricity_cooling_kwh']
    
    # Water heating
    df['water_heating'] = df['electricity_water_systems_kwh']
    
    # Refrigerator
    df['refrigerator'] = df['electricity_refrigerator_kwh']
    
    # Clothes washer
    df['clothes_washer'] = df['electricity_clothes_washer_kwh']
    
    # Clothes dryer
    df['clothes_dryer'] = df['electricity_clothes_dryer_kwh']
    
    # Dishwasher
    df['dishwasher'] = df['electricity_dishwasher_kwh']
    
    # Cooking range
    df['cooking_range'] = df['electricity_cooking_range_kwh']
    
    # Pool/Spa Pumps
    df['pool_spa_pumps'] = df['electricity_pool_pump_kwh'] + df['electricity_hot_tub_pump_kwh']
    
    # Interior Lighting
    df['interior_lighting'] = df['electricity_interior_lighting_kwh']
    
    # Exterior Lighting
    df['exterior_lighting'] = df['electricity_exterior_lighting_kwh']
    
    # Total Lighting
    df['lighting'] = df['interior_lighting'] + df['exterior_lighting']
    
    # Plug loads
    df['plug'] = df['electricity_plug_loads_kwh']
    
    # Pool/Spa Heaters
    df['pool_spa_heaters'] = df['electricity_pool_heater_kwh'] + df['electricity_hot_tub_heater_kwh']
    
    # 5. Aggregate
    agg_dict = {
        'hvac': 'sum',
        'water_heating': 'sum',
        'refrigerator': 'sum',
        'clothes_washer': 'sum',
        'clothes_dryer': 'sum',
        'dishwasher': 'sum',
        'cooking_range': 'sum',
        'pool_spa_pumps': 'sum',
        'interior_lighting': 'sum',
        'exterior_lighting': 'sum',
        'lighting': 'sum',
        'plug': 'sum',
        'pool_spa_heaters': 'sum'
    }
    
    result = df.groupby(['season', 'hour']).agg(agg_dict).reset_index()
    
    # 6. Ensure column order and types
    target_columns = [
        'season', 'hour', 'hvac', 'water_heating', 'refrigerator', 
        'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 
        'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
        'lighting', 'plug', 'pool_spa_heaters'
    ]
    
    result = result[target_columns]
    
    # Ensure hour is int64
    result['hour'] = result['hour'].astype('int64')
    
    return result
