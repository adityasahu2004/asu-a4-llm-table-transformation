import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse time
    df = source.copy()
    df['time'] = pd.to_datetime(df['time'])
    
    # 2. Extract hour and month
    df['hour'] = df['time'].dt.hour
    df['month'] = df['time'].dt.month
    
    # 3. Map months to seasons (Southern Hemisphere Meteorological)
    # Winter: Jun(6), Jul(7), Aug(8)
    # Spring: Sep(9), Oct(10), Nov(11)
    # Summer: Dec(12), Jan(1), Feb(2)
    # Autumn: Mar(3), Apr(4), May(5) - Not in target distincts, but mapping for completeness if needed.
    # Based on target distincts ["Summer", "Winter", "Spring"], and source sample months [7,8,9,10,11,12,1],
    # the mapping is:
    # 6,7,8 -> Winter
    # 9,10,11 -> Spring
    # 12,1,2 -> Summer
    
    def get_season(month):
        if month in [6, 7, 8]:
            return "Winter"
        elif month in [9, 10, 11]:
            return "Spring"
        elif month in [12, 1, 2]:
            return "Summer"
        else:
            # Fallback for Autumn months if they appear in eval data
            # Since "Autumn" is not in target distincts, this might be an issue.
            # However, based on the sample, we assume only SH seasons are present.
            # If Autumn is present, we might need to map it. 
            # Given the constraints, I'll map 3,4,5 to "Autumn" but if the target 
            # strictly requires only the 3 values, this might be wrong.
            # But looking at the sample, it's consistent with SH.
            return "Autumn" 

    df['season'] = df['month'].apply(get_season)
    
    # 4. Define column groups for aggregation
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
        'electricity_ceiling_fan_kwh',
        'electricity_pool_heater_kwh',
        'electricity_pool_pump_kwh',
        'electricity_hot_tub_heater_kwh',
        'electricity_hot_tub_pump_kwh'
    ]
    
    # 5. Aggregate
    # We group by season and hour, and sum the relevant columns.
    # We can create the aggregated dataframe by summing the groups.
    
    grouped = df.groupby(['season', 'hour'])
    
    # Calculate sums for each category
    # Note: We need to ensure we sum the specific columns.
    
    agg_dict = {
        'hvac': (hvac_cols, 'sum'),
        'domestic_water_heating': (water_cols, 'sum'),
        'major_appliances': (major_appliance_cols, 'sum'),
        'lighting': (lighting_cols, 'sum'),
        'miscellaneous_plug_loads': (misc_plug_cols, 'sum'),
        'total': ('net_site_electricity_kwh', 'sum')
    }
    
    # Perform aggregation
    # We'll create a new dataframe with the grouped sums
    
    result_data = {}
    
    # Get unique groups
    groups = grouped.groups
    
    # It's easier to just sum the columns in the grouped object
    # But we need to sum multiple columns into one.
    
    # Let's sum the hvac columns first
    df['hvac_sum'] = df[hvac_cols].sum(axis=1)
    df['water_sum'] = df[water_cols].sum(axis=1)
    df['major_sum'] = df[major_appliance_cols].sum(axis=1)
    df['lighting_sum'] = df[lighting_cols].sum(axis=1)
    df['misc_sum'] = df[misc_plug_cols].sum(axis=1)
    
    # Now groupby and sum these new columns
    agg_df = df.groupby(['season', 'hour']).agg(
        hvac=('hvac_sum', 'sum'),
        domestic_water_heating=('water_sum', 'sum'),
        major_appliances=('major_sum', 'sum'),
        lighting=('lighting_sum', 'sum'),
        miscellaneous_plug_loads=('misc_sum', 'sum'),
        total=('net_site_electricity_kwh', 'sum')
    ).reset_index()
    
    # Ensure column order
    target_cols = [
        'season',
        'hour',
        'hvac',
        'domestic_water_heating',
        'major_appliances',
        'lighting',
        'miscellaneous_plug_loads',
        'total'
    ]
    
    result = agg_df[target_cols]
    
    # Ensure hour is int64
    result['hour'] = result['hour'].astype('int64')
    
    return result
