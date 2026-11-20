import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    dt = pd.to_datetime(source['time'], format='%Y-%m-%d %H:%M:%S.%f')
    out = pd.DataFrame(index=source.index)
    out['datetime'] = dt.strftime('%Y-%m-%d %H:%M:%S')
    
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
    
    # Calculate HVAC
    hvac_sum = source[hvac_cols].sum(axis=1)
    out['hvac'] = hvac_sum.values
    
    # Water heating
    out['water_heating'] = source['electricity_water_systems_kwh'].values
    
    # Appliances
    out['refrigerator'] = source['electricity_refrigerator_kwh'].values
    out['clothes_washer'] = source['electricity_clothes_washer_kwh'].values
    out['clothes_dryer'] = source['electricity_clothes_dryer_kwh'].values
    out['dishwasher'] = source['electricity_dishwasher_kwh'].values
    out['cooking_range'] = source['electricity_cooking_range_kwh'].values
    
    # Pool/Spa Pumps
    out['pool_spa_pumps'] = (source['electricity_pool_pump_kwh'] + source['electricity_hot_tub_pump_kwh']).values
    
    # Lighting
    out['interior_lighting'] = source['electricity_interior_lighting_kwh'].values
    out['exterior_lighting'] = source['electricity_exterior_lighting_kwh'].values
    out['lighting'] = (out['interior_lighting'] + out['exterior_lighting']).values
    
    # Plug
    out['plug'] = source['electricity_plug_loads_kwh'].values
    
    # Pool/Spa Heater
    out['pool_spa_heater'] = (source['electricity_pool_heater_kwh'] + source['electricity_hot_tub_heater_kwh']).values
    
    return out.reset_index(drop=True)
