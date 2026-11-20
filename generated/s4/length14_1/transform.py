import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse time
    source = source.copy()
    source['time_dt'] = pd.to_datetime(source['time'])
    
    # Extract grouping keys
    source['month'] = source['time_dt'].dt.month
    source['hour'] = source['time_dt'].dt.hour
    
    # Define aggregation logic
    agg_dict = {
        # HVAC: Heating + Cooling + Fans (Heating/Cooling) + Pumps (Heating/Cooling)
        # Note: electricity_pumps_cooling_kwh is constant 0, but included for completeness if needed.
        # Central system components are distinct columns.
        'electricity_heating_kwh': 'sum',
        'electricity_central_system_heating_kwh': 'sum',
        'electricity_cooling_kwh': 'sum',
        'electricity_central_system_cooling_kwh': 'sum',
        'electricity_fans_heating_kwh': 'sum',
        'electricity_fans_cooling_kwh': 'sum',
        'electricity_pumps_heating_kwh': 'sum',
        'electricity_central_system_pumps_heating_kwh': 'sum',
        'electricity_pumps_cooling_kwh': 'sum',
        'electricity_central_system_pumps_cooling_kwh': 'sum',
        
        # Domestic Water Heating
        'electricity_water_systems_kwh': 'sum',
        
        # Major Appliances
        'electricity_refrigerator_kwh': 'sum',
        'electricity_clothes_washer_kwh': 'sum',
        'electricity_clothes_dryer_kwh': 'sum',
        'electricity_cooking_range_kwh': 'sum',
        'electricity_dishwasher_kwh': 'sum',
        
        # Lighting
        'electricity_interior_lighting_kwh': 'sum',
        'electricity_exterior_lighting_kwh': 'sum',
        
        # Miscellaneous Plug Loads
        'electricity_plug_loads_kwh': 'sum',
        'electricity_house_fan_kwh': 'sum',
        'electricity_range_fan_kwh': 'sum',
        'electricity_bath_fan_kwh': 'sum',
        'electricity_ceiling_fan_kwh': 'sum',
        'electricity_pool_heater_kwh': 'sum',
        'electricity_pool_pump_kwh': 'sum',
        'electricity_hot_tub_heater_kwh': 'sum',
        'electricity_hot_tub_pump_kwh': 'sum',
        
        # Total
        'net_site_electricity_kwh': 'sum'
    }
    
    grouped = source.groupby(['month', 'hour']).agg(agg_dict).reset_index()
    
    # Construct target columns
    hvac_cols = [
        'electricity_heating_kwh', 'electricity_central_system_heating_kwh',
        'electricity_cooling_kwh', 'electricity_central_system_cooling_kwh',
        'electricity_fans_heating_kwh', 'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh', 'electricity_central_system_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh', 'electricity_central_system_pumps_cooling_kwh'
    ]
    
    water_cols = ['electricity_water_systems_kwh']
    
    major_appliance_cols = [
        'electricity_refrigerator_kwh', 'electricity_clothes_washer_kwh',
        'electricity_clothes_dryer_kwh', 'electricity_cooking_range_kwh',
        'electricity_dishwasher_kwh'
    ]
    
    lighting_cols = [
        'electricity_interior_lighting_kwh', 'electricity_exterior_lighting_kwh'
    ]
    
    misc_plug_cols = [
        'electricity_plug_loads_kwh', 'electricity_house_fan_kwh',
        'electricity_range_fan_kwh', 'electricity_bath_fan_kwh',
        'electricity_ceiling_fan_kwh', 'electricity_pool_heater_kwh',
        'electricity_pool_pump_kwh', 'electricity_hot_tub_heater_kwh',
        'electricity_hot_tub_pump_kwh'
    ]
    
    target_df = pd.DataFrame()
    target_df['month'] = grouped['month']
    target_df['hour'] = grouped['hour']
    target_df['hvac'] = grouped[hvac_cols].sum(axis=1)
    target_df['domestic_water_heating'] = grouped[water_cols].sum(axis=1)
    target_df['major_appliances'] = grouped[major_appliance_cols].sum(axis=1)
    target_df['lighting'] = grouped[lighting_cols].sum(axis=1)
    target_df['miscellaneous_plug_loads'] = grouped[misc_plug_cols].sum(axis=1)
    target_df['total'] = grouped['net_site_electricity_kwh']
    
    # Ensure correct dtypes
    target_df['month'] = target_df['month'].astype('int64')
    target_df['hour'] = target_df['hour'].astype('int64')
    
    return target_df
