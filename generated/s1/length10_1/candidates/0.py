import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Create datetime column
    # Source time format: "2012-07-02 00:15:00.000"
    # Target datetime format: "2012-01-01 00:15:00"
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Calculate hvac
    # Includes heating, cooling, fans, pumps, and house fan
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
        'electricity_central_system_pumps_cooling_kwh',
        'electricity_house_fan_kwh'
    ]
    df['hvac'] = df[hvac_cols].sum(axis=1)
    
    # 3. Water heating
    df['water_heating'] = df['electricity_water_systems_kwh']
    
    # 4. Refrigerator
    df['refrigerator'] = df['electricity_refrigerator_kwh']
    
    # 5. Clothes washer
    df['clothes_washer'] = df['electricity_clothes_washer_kwh']
    
    # 6. Clothes dryer
    df['clothes_dryer'] = df['electricity_clothes_dryer_kwh']
    
    # 7. Dishwasher
    df['dishwasher'] = df['electricity_dishwasher_kwh']
    
    # 8. Cooking range
    df['cooking_range'] = df['electricity_cooking_range_kwh']
    
    # 9. Pool/Spa Pumps
    df['pool_spa_pumps'] = df['electricity_pool_pump_kwh'] + df['electricity_hot_tub_pump_kwh']
    
    # 10. Interior Lighting
    df['interior_lighting'] = df['electricity_interior_lighting_kwh']
    
    # 11. Exterior Lighting
    df['exterior_lighting'] = df['electricity_exterior_lighting_kwh']
    
    # 12. Lighting (Total)
    df['lighting'] = df['interior_lighting'] + df['exterior_lighting']
    
    # 13. Plug Loads
    # Includes plug loads and various fans (range, bath, ceiling)
    plug_cols = [
        'electricity_plug_loads_kwh',
        'electricity_range_fan_kwh',
        'electricity_bath_fan_kwh',
        'electricity_ceiling_fan_kwh'
    ]
    df['plug'] = df[plug_cols].sum(axis=1)
    
    # 14. Pool/Spa Heater
    df['pool_spa_heater'] = df['electricity_pool_heater_kwh'] + df['electricity_hot_tub_heater_kwh']
    
    # Select and order columns as per target
    target_columns = [
        'datetime',
        'hvac',
        'water_heating',
        'refrigerator',
        'clothes_washer',
        'clothes_dryer',
        'dishwasher',
        'cooking_range',
        'pool_spa_pumps',
        'interior_lighting',
        'exterior_lighting',
        'lighting',
        'plug',
        'pool_spa_heater'
    ]
    
    result = df[target_columns]
    
    return result
