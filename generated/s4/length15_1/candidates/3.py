import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse time
    dt = pd.to_datetime(source['time'])
    hours = dt.dt.hour
    months = dt.dt.month
    
    # Define seasons
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else: # 9, 10, 11
            return 'Fall'
            
    seasons = months.apply(get_season)
    
    # Create a temporary dataframe for calculations
    df = pd.DataFrame({
        'season': seasons,
        'hour': hours,
        'hvac': (
            source['electricity_heating_kwh'] +
            source['electricity_cooling_kwh'] +
            source['electricity_fans_heating_kwh'] +
            source['electricity_fans_cooling_kwh'] +
            source['electricity_pumps_heating_kwh'] +
            source['electricity_pumps_cooling_kwh'] +
            source['electricity_central_system_heating_kwh'] +
            source['electricity_central_system_cooling_kwh'] +
            source['electricity_central_system_pumps_heating_kwh'] +
            source['electricity_central_system_pumps_cooling_kwh'] +
            source['electricity_pool_heater_kwh'] +
            source['electricity_pool_pump_kwh'] +
            source['electricity_hot_tub_heater_kwh'] +
            source['electricity_hot_tub_pump_kwh']
        ),
        'domestic_water_heating': source['electricity_water_systems_kwh'],
        'major_appliances': (
            source['electricity_refrigerator_kwh'] +
            source['electricity_clothes_washer_kwh'] +
            source['electricity_clothes_dryer_kwh'] +
            source['electricity_cooking_range_kwh'] +
            source['electricity_dishwasher_kwh']
        ),
        'lighting': (
            source['electricity_interior_lighting_kwh'] +
            source['electricity_exterior_lighting_kwh']
        ),
        'miscellaneous_plug_loads': (
            source['electricity_plug_loads_kwh'] +
            source['electricity_house_fan_kwh'] +
            source['electricity_range_fan_kwh'] +
            source['electricity_bath_fan_kwh'] +
            source['electricity_ceiling_fan_kwh']
        ),
        'total': source['net_site_electricity_kwh']
    })
    
    # Group by season and hour, and sum the values
    result = df.groupby(['season', 'hour'], as_index=False).sum()
    
    # Ensure column order
    cols = ['season', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    result = result[cols]
    
    return result
