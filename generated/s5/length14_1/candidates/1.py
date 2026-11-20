import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse time
    source['dt'] = pd.to_datetime(source['time'])
    
    # Define groups for aggregation
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_central_system_pumps_heating_kwh',
        'electricity_central_system_pumps_cooling_kwh',
        'electricity_pool_heater_kwh',
        'electricity_pool_pump_kwh',
        'electricity_hot_tub_heater_kwh',
        'electricity_hot_tub_pump_kwh'
    ]
    
    # Check for central system heating/cooling. In many BEP datasets, these are subsets of the main heating/cooling 
    # or specific equipment. However, 'electricity_heating_kwh' and 'electricity_cooling_kwh' usually represent the total load for those categories.
    # Let's stick to the explicit components listed above which are clearly HVAC mechanicals.
    
    water_cols = [
        'electricity_water_systems_kwh'
    ]
    
    major_appliance_cols = [
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
        'electricity_ceiling_fan_kwh'
    ]
    
    # Create temporary columns for sums
    source['hvac'] = source[hvac_cols].sum(axis=1)
    source['domestic_water_heating'] = source[water_cols].sum(axis=1)
    source['major_appliances'] = source[major_appliance_cols].sum(axis=1)
    source['lighting'] = source[lighting_cols].sum(axis=1)
    source['miscellaneous_plug_loads'] = source[misc_plug_cols].sum(axis=1)
    source['total'] = source['net_site_electricity_kwh']
    
    # Group and aggregate
    agg_df = source.groupby([source['dt'].dt.month, source['dt'].dt.hour]).agg(
        hvac=('hvac', 'sum'),
        domestic_water_heating=('domestic_water_heating', 'sum'),
        major_appliances=('major_appliances', 'sum'),
        lighting=('lighting', 'sum'),
        miscellaneous_plug_loads=('miscellaneous_plug_loads', 'sum'),
        total=('total', 'sum')
    ).reset_index()
    
    # Rename columns to match target
    agg_df.rename(columns={
        'month': 'month',
        'hour': 'hour',
    }, inplace=True)
    
    # Ensure correct column order
    result = agg_df[['month', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    # Ensure integer types for month and hour
    result['month'] = result['month'].astype('int64')
    result['hour'] = result['hour'].astype('int64')
    
    return result
