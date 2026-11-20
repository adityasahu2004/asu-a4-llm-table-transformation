import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse time and format as YYYY-MM-DD HH:MM:SS
    dt = pd.to_datetime(source['time'])
    out = pd.DataFrame(index=source.index)
    out['datetime'] = dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # HVAC: Heating + Cooling + Fans + Pumps (non-central system end-uses)
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh'
    ]
    out['hvac'] = source[hvac_cols].sum(axis=1)
    
    # Domestic Water Heating
    out['domestic_water_heating'] = source['electricity_water_systems_kwh']
    
    # Major Appliances
    appliance_cols = [
        'electricity_refrigerator_kwh',
        'electricity_clothes_washer_kwh',
        'electricity_clothes_dryer_kwh',
        'electricity_cooking_range_kwh',
        'electricity_dishwasher_kwh'
    ]
    out['major_appliances'] = source[appliance_cols].sum(axis=1)
    
    # Lighting
    lighting_cols = [
        'electricity_interior_lighting_kwh',
        'electricity_exterior_lighting_kwh'
    ]
    out['lighting'] = source[lighting_cols].sum(axis=1)
    
    # Miscellaneous Plug Loads (Plug loads + Fans that are not HVAC fans)
    plug_cols = [
        'electricity_plug_loads_kwh',
        'electricity_house_fan_kwh',
        'electricity_range_fan_kwh',
        'electricity_bath_fan_kwh',
        'electricity_ceiling_fan_kwh'
    ]
    out['miscellaneous_plug_loads'] = source[plug_cols].sum(axis=1)
    
    # Total
    out['total'] = out['hvac'] + out['domestic_water_heating'] + out['major_appliances'] + out['lighting'] + out['miscellaneous_plug_loads']
    
    return out.reset_index(drop=True)
