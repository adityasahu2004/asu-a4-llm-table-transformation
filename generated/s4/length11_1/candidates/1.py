import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse time
    dt = pd.to_datetime(source['time'])
    
    out = pd.DataFrame(index=source.index)
    out['month'] = dt.dt.month
    out['hour'] = dt.dt.hour
    
    # HVAC components
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
    out['hvac'] = source[hvac_cols].sum(axis=1)
    
    # Water heating
    out['water_heating'] = source['electricity_water_systems_kwh']
    
    # Appliances
    out['refrigerator'] = source['electricity_refrigerator_kwh']
    out['clothes_washer'] = source['electricity_clothes_washer_kwh']
    out['clothes_dryer'] = source['electricity_clothes_dryer_kwh']
    out['dishwasher'] = source['electricity_dishwasher_kwh']
    out['cooking_range'] = source['electricity_cooking_range_kwh']
    
    # Pool/Spa Pumps
    out['pool_spa_pumps'] = source['electricity_pool_pump_kwh'] + source['electricity_hot_tub_pump_kwh']
    
    # Lighting
    out['interior_lighting'] = source['electricity_interior_lighting_kwh']
    out['exterior_lighting'] = source['electricity_exterior_lighting_kwh']
    out['lighting'] = out['interior_lighting'] + out['exterior_lighting']
    
    # Plug loads
    out['plug'] = source['electricity_plug_loads_kwh']
    
    # Pool/Spa Heater
    out['pool_spa_heater'] = source['electricity_pool_heater_kwh'] + source['electricity_hot_tub_heater_kwh']
    
    # Select and order columns
    cols = [
        'month', 'hour', 'hvac', 'water_heating', 'refrigerator', 
        'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 
        'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
        'lighting', 'plug', 'pool_spa_heater'
    ]
    
    return out[cols].reset_index(drop=True)
