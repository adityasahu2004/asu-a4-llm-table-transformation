import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse time
    source = source.copy()
    source['time_dt'] = pd.to_datetime(source['time'])
    source['month'] = source['time_dt'].dt.month
    source['hour'] = source['time_dt'].dt.hour

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
    source['hvac'] = source[hvac_cols].sum(axis=1)

    # Define Domestic Water Heating components
    dwh_cols = [
        'electricity_water_systems_kwh',
        'electricity_pool_heater_kwh',
        'electricity_pool_pump_kwh',
        'electricity_hot_tub_heater_kwh',
        'electricity_hot_tub_pump_kwh'
    ]
    source['domestic_water_heating'] = source[dwh_cols].sum(axis=1)

    # Define Major Appliances components
    ma_cols = [
        'electricity_refrigerator_kwh',
        'electricity_clothes_washer_kwh',
        'electricity_clothes_dryer_kwh',
        'electricity_cooking_range_kwh',
        'electricity_dishwasher_kwh'
    ]
    source['major_appliances'] = source[ma_cols].sum(axis=1)

    # Define Lighting components
    lighting_cols = [
        'electricity_interior_lighting_kwh',
        'electricity_exterior_lighting_kwh'
    ]
    source['lighting'] = source[lighting_cols].sum(axis=1)

    # Define Miscellaneous Plug Loads components
    mpl_cols = [
        'electricity_plug_loads_kwh',
        'electricity_house_fan_kwh',
        'electricity_range_fan_kwh',
        'electricity_bath_fan_kwh',
        'electricity_ceiling_fan_kwh'
    ]
    source['miscellaneous_plug_loads'] = source[mpl_cols].sum(axis=1)

    # Define Total
    source['total'] = source['net_site_electricity_kwh']

    # Group by month and hour and sum
    agg_df = source.groupby(['month', 'hour']).agg(
        hvac=('hvac', 'sum'),
        domestic_water_heating=('domestic_water_heating', 'sum'),
        major_appliances=('major_appliances', 'sum'),
        lighting=('lighting', 'sum'),
        miscellaneous_plug_loads=('miscellaneous_plug_loads', 'sum'),
        total=('total', 'sum')
    ).reset_index()

    return agg_df
