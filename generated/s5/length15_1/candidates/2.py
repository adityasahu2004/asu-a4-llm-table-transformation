import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse time
    df = source.copy()
    df['time_dt'] = pd.to_datetime(df['time'])
    df['hour'] = df['time_dt'].dt.hour
    df['month'] = df['time_dt'].dt.month
    
    # Determine Season
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
            
    df['season'] = df['month'].apply(get_season)
    
    # Define aggregation groups
    hvac_cols = [
        'electricity_heating_kwh', 'electricity_cooling_kwh',
        'electricity_fans_heating_kwh', 'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh', 'electricity_central_system_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh', 'electricity_central_system_pumps_cooling_kwh'
    ]
    
    dwhe_cols = ['electricity_water_systems_kwh']
    
    major_appl_cols = [
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
    
    total_col = 'net_site_electricity_kwh'
    
    # Create scaled values for aggregation
    # We need to sum (value * scale). 
    # Since scale is constant, sum(value) * scale is also valid, but let's do element-wise mult to be safe.
    scale = df['scaled_unit_count']
    
    df['hvac_scaled'] = df[hvac_cols].sum(axis=1) * scale
    df['dwhe_scaled'] = df[dwhe_cols].sum(axis=1) * scale
    df['major_appl_scaled'] = df[major_appl_cols].sum(axis=1) * scale
    df['lighting_scaled'] = df[lighting_cols].sum(axis=1) * scale
    df['misc_plug_scaled'] = df[misc_plug_cols].sum(axis=1) * scale
    df['total_scaled'] = df[total_col] * scale
    
    # Group by season and hour
    agg_data = df.groupby(['season', 'hour']).agg(
        hvac=('hvac_scaled', 'sum'),
        domestic_water_heating=('dwhe_scaled', 'sum'),
        major_appliances=('major_appl_scaled', 'sum'),
        lighting=('lighting_scaled', 'sum'),
        miscellaneous_plug_loads=('misc_plug_scaled', 'sum'),
        total=('total_scaled', 'sum')
    ).reset_index()
    
    # Select and order columns
    result = agg_data[['season', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    return result
