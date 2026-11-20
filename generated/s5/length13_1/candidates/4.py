import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse time and format
    dt = pd.to_datetime(source['time'])
    out = pd.DataFrame()
    out['datetime'] = dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Define column groups for aggregation
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
    
    major_appliances_cols = [
        'electricity_refrigerator_kwh',
        'electricity_clothes_washer_kwh',
        'electricity_clothes_dryer_kwh',
        'electricity_cooking_range_kwh',
        'electricity_dishwasher_kwh'
    ]
    
    lighting_cols = [
        'electricity_interior_lighting_kwh',
        'electricity_exterior_lighting_kwh'
    ]
    
    misc_plug_cols = [
        'electricity_plug_loads_kwh',
        'electricity_house_fan_kwh',
        'electricity_range_fan_kwh',
        'electricity_bath_fan_kwh',
        'electricity_ceiling_fan_kwh',
        'electricity_pool_heater_kwh',
        'electricity_pool_pump_kwh',
        'electricity_hot_tub_heater_kwh',
        'electricity_hot_tub_pump_kwh'
    ]
    
    # Calculate aggregates
    out['hvac'] = source[hvac_cols].sum(axis=1)
    out['domestic_water_heating'] = source['electricity_water_systems_kwh']
    out['major_appliances'] = source[major_appliances_cols].sum(axis=1)
    out['lighting'] = source[lighting_cols].sum(axis=1)
    out['miscellaneous_plug_loads'] = source[misc_plug_cols].sum(axis=1)
    out['total'] = source['net_site_electricity_kwh']
    
    return out
