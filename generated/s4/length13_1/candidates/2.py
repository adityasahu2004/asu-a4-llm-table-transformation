import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    dt = pd.to_datetime(source['time'])
    datetime_str = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # HVAC Components
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
    hvac = source[hvac_cols].sum(axis=1)
    
    # Domestic Water Heating
    domestic_water_heating = source['electricity_water_systems_kwh']
    
    # Major Appliances
    major_appliance_cols = [
        'electricity_refrigerator_kwh',
        'electricity_clothes_washer_kwh',
        'electricity_clothes_dryer_kwh',
        'electricity_cooking_range_kwh',
        'electricity_dishwasher_kwh'
    ]
    major_appliances = source[major_appliance_cols].sum(axis=1)
    
    # Lighting
    lighting_cols = [
        'electricity_interior_lighting_kwh',
        'electricity_exterior_lighting_kwh'
    ]
    lighting = source[lighting_cols].sum(axis=1)
    
    # Miscellaneous Plug Loads
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
    miscellaneous_plug_loads = source[misc_plug_cols].sum(axis=1)
    
    # Total
    total = source['net_site_electricity_kwh']
    
    # Construct Result
    result = pd.DataFrame({
        'datetime': datetime_str,
        'hvac': hvac,
        'domestic_water_heating': domestic_water_heating,
        'major_appliances': major_appliances,
        'lighting': lighting,
        'miscellaneous_plug_loads': miscellaneous_plug_loads,
        'total': total
    })
    
    return result.reset_index(drop=True)
