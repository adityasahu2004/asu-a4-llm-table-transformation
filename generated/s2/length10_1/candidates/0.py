import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse time
    dt = pd.to_datetime(source['time'])
    
    # HVAC Calculation
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh',
        'electricity_central_system_heating_kwh',
        'electricity_central_system_cooling_kwh',
        'electricity_central_system_pumps_heating_kwh',
        'electricity_central_system_pumps_cooling_kwh'
    ]
    hvac = source[hvac_cols].sum(axis=1)
    
    # Water Heating
    water_heating = source['electricity_water_systems_kwh']
    
    # Appliances
    refrigerator = source['electricity_refrigerator_kwh']
    clothes_washer = source['electricity_clothes_washer_kwh']
    clothes_dryer = source['electricity_clothes_dryer_kwh']
    dishwasher = source['electricity_dishwasher_kwh']
    cooking_range = source['electricity_cooking_range_kwh']
    
    # Pool/Spa Pumps
    pool_spa_pumps = source['electricity_pool_pump_kwh'] + source['electricity_hot_tub_pump_kwh']
    
    # Lighting
    interior_lighting = source['electricity_interior_lighting_kwh']
    exterior_lighting = source['electricity_exterior_lighting_kwh']
    lighting = interior_lighting + exterior_lighting
    
    # Plug
    plug = source['electricity_plug_loads_kwh']
    
    # Pool/Spa Heater
    pool_spa_heater = source['electricity_pool_heater_kwh'] + source['electricity_hot_tub_heater_kwh']
    
    # Construct Result
    result = pd.DataFrame({
        'datetime': dt.dt.strftime('%Y-%m-%d %H:%M:%S'),
        'hvac': hvac,
        'water_heating': water_heating,
        'refrigerator': refrigerator,
        'clothes_washer': clothes_washer,
        'clothes_dryer': clothes_dryer,
        'dishwasher': dishwasher,
        'cooking_range': cooking_range,
        'pool_spa_pumps': pool_spa_pumps,
        'interior_lighting': interior_lighting,
        'exterior_lighting': exterior_lighting,
        'lighting': lighting,
        'plug': plug,
        'pool_spa_heater': pool_spa_heater
    })
    
    return result
