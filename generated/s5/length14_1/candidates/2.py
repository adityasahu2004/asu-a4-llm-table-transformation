import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse time to extract month and hour
    source = source.copy()
    source['time_dt'] = pd.to_datetime(source['time'])
    source['month'] = source['time_dt'].dt.month
    source['hour'] = source['time_dt'].dt.hour
    
    # Define aggregation groups
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_central_system_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh',
        'electricity_central_system_pumps_cooling_kwh',
        'electricity_house_fan_kwh',
        'electricity_range_fan_kwh',
        'electricity_bath_fan_kwh',
        'electricity_ceiling_fan_kwh',
        'electricity_pool_heater_kwh',
        'electricity_pool_pump_kwh',
        'electricity_hot_tub_heater_kwh',
        'electricity_hot_tub_pump_kwh'
    ]
    
    water_cols = ['electricity_water_systems_kwh']
    
    major_appl_cols = [
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
    
    misc_plug_cols = ['electricity_plug_loads_kwh']
    
    total_cols = ['net_site_electricity_kwh']
    
    # Group by month and hour, then sum the relevant columns
    grouped = source.groupby(['month', 'hour'])
    
    result = pd.DataFrame()
    result['month'] = grouped.first()['month'] # Just to get the index back if needed, but reset_index handles it
    result['hour'] = grouped.first()['hour']
    
    # Actually, simpler to aggregate directly into a dataframe
    agg_dict = {
        'hvac': (hvac_cols, 'sum'),
        'domestic_water_heating': (water_cols, 'sum'),
        'major_appliances': (major_appl_cols, 'sum'),
        'lighting': (lighting_cols, 'sum'),
        'miscellaneous_plug_loads': (misc_plug_cols, 'sum'),
        'total': (total_cols, 'sum')
    }
    
    # Perform aggregation
    df_agg = grouped.agg(
        hvac=(hvac_cols, 'sum'),
        domestic_water_heating=(water_cols, 'sum'),
        major_appliances=(major_appl_cols, 'sum'),
        lighting=(lighting_cols, 'sum'),
        miscellaneous_plug_loads=(misc_plug_cols, 'sum'),
        total=(total_cols, 'sum')
    ).reset_index()
    
    # Ensure column order matches target
    target_cols = [
        'month', 
        'hour', 
        'hvac', 
        'domestic_water_heating', 
        'major_appliances', 
        'lighting', 
        'miscellaneous_plug_loads', 
        'total'
    ]
    
    return df_agg[target_cols]
