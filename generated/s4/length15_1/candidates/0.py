import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse time
    dt = pd.to_datetime(source['time'])
    source = source.copy()
    source['hour'] = dt.dt.hour
    source['month'] = dt.dt.month
    
    # Map month to season
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall' # Not in target, but good practice
            
    source['season'] = source['month'].apply(get_season)
    
    # Define columns for each category
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
    
    dwh_cols = [
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
        'electricity_ceiling_fan_kwh',
        'electricity_pool_heater_kwh',
        'electricity_pool_pump_kwh',
        'electricity_hot_tub_heater_kwh',
        'electricity_hot_tub_pump_kwh'
    ]
    
    # Group by season and hour
    grouped = source.groupby(['season', 'hour'])
    
    # Aggregate
    agg_df = grouped.agg(
        hvac=(hvac_cols[0], 'sum'), # Placeholder, will calculate sum of all cols
        domestic_water_heating=(dwh_cols[0], 'sum'),
        major_appliances=(major_appliance_cols[0], 'sum'),
        lighting=(lighting_cols[0], 'sum'),
        miscellaneous_plug_loads=(misc_plug_cols[0], 'sum'),
        total=('net_site_electricity_kwh', 'sum')
    ).reset_index()
    
    # Calculate specific sums for multi-column categories
    # Since agg doesn't easily sum multiple columns into one new column in one step without custom func,
    # we can do it manually or use apply. Given the structure, let's sum them explicitly from the grouped object or original data.
    
    # Re-grouping to sum specific lists of columns
    def sum_cols(group, cols):
        return group[cols].sum(axis=1).sum()

    # It's cleaner to just sum the columns in the source dataframe per group
    agg_hvac = grouped[hvac_cols].sum().sum(axis=1)
    agg_dwh = grouped[dwh_cols].sum().sum(axis=1)
    agg_maj = grouped[major_appliance_cols].sum().sum(axis=1)
    agg_light = grouped[lighting_cols].sum().sum(axis=1)
    agg_misc = grouped[misc_plug_cols].sum().sum(axis=1)
    agg_total = grouped['net_site_electricity_kwh'].sum()
    
    result = pd.DataFrame({
        'hvac': agg_hvac.values,
        'domestic_water_heating': agg_dwh.values,
        'major_appliances': agg_maj.values,
        'lighting': agg_light.values,
        'miscellaneous_plug_loads': agg_misc.values,
        'total': agg_total.values
    }, index=agg_hvac.index)
    
    result = result.reset_index()
    
    # Ensure column order and names
    result = result[['season', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    # Sort by season and hour to match potential target order, though target sample is not sorted strictly.
    # The target sample order is random. We will just return the dataframe.
    
    return result
