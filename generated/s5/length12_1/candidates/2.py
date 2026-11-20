import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse time
    df = source.copy()
    df['time_dt'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S.%f')
    df['hour'] = df['time_dt'].dt.hour
    df['month'] = df['time_dt'].dt.month
    
    # Determine season
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
    
    # Define HVAC components
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_central_system_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_central_system_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_central_system_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh',
        'electricity_central_system_pumps_cooling_kwh'
    ]
    
    # Define other components
    lighting_cols = ['electricity_interior_lighting_kwh', 'electricity_exterior_lighting_kwh']
    pool_spa_pump_cols = ['electricity_pool_pump_kwh', 'electricity_hot_tub_pump_kwh']
    pool_spa_heater_cols = ['electricity_pool_heater_kwh', 'electricity_hot_tub_heater_kwh']
    
    # Calculate intermediate sums
    df['hvac'] = df[hvac_cols].sum(axis=1)
    df['water_heating'] = df['electricity_water_systems_kwh']
    df['refrigerator'] = df['electricity_refrigerator_kwh']
    df['clothes_washer'] = df['electricity_clothes_washer_kwh']
    df['clothes_dryer'] = df['electricity_clothes_dryer_kwh']
    df['dishwasher'] = df['electricity_dishwasher_kwh']
    df['cooking_range'] = df['electricity_cooking_range_kwh']
    df['pool_spa_pumps'] = df[pool_spa_pump_cols].sum(axis=1)
    df['interior_lighting'] = df['electricity_interior_lighting_kwh']
    df['exterior_lighting'] = df['electricity_exterior_lighting_kwh']
    df['lighting'] = df[lighting_cols].sum(axis=1)
    df['plug'] = df['electricity_plug_loads_kwh']
    df['pool_spa_heaters'] = df[pool_spa_heater_cols].sum(axis=1)
    
    # Select columns for grouping
    agg_cols = [
        'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer',
        'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting',
        'exterior_lighting', 'lighting', 'plug', 'pool_spa_heaters'
    ]
    
    # Group by season and hour
    result = df.groupby(['season', 'hour'])[agg_cols].sum().reset_index()
    
    # Sort for deterministic output order (optional but good practice)
    result = result.sort_values(['season', 'hour']).reset_index(drop=True)
    
    return result
