import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse time
    source = source.copy()
    source['time_dt'] = pd.to_datetime(source['time'])
    
    # 2. Extract month and hour
    source['month'] = source['time_dt'].dt.month
    source['hour'] = source['time_dt'].dt.hour
    
    # 3. Define column mappings for aggregation
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
    
    major_appliances_cols = [
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
    
    # 4. Aggregate by month and hour
    agg_dict = {
        'hvac': (hvac_cols, 'sum'),
        'domestic_water_heating': (dwh_cols, 'sum'),
        'major_appliances': (major_appliances_cols, 'sum'),
        'lighting': (lighting_cols, 'sum'),
        'miscellaneous_plug_loads': (misc_plug_cols, 'sum')
    }
    
    # Perform aggregation
    # We need to sum specific columns for each group
    grouped = source.groupby(['month', 'hour'])
    
    # Create a dataframe for the aggregated results
    result = pd.DataFrame()
    result['month'] = grouped.groups.keys() # This is a bit tricky, better to use agg
    
    # Let's use agg with a custom function or multiple sums
    # Since we have many columns, let's sum them individually first or use a loop
    
    # Initialize result dataframe with index
    indices = grouped.groups.keys()
    result = pd.DataFrame(list(indices), columns=['month', 'hour'])
    
    # Calculate sums for each category
    for col_name, (cols, func) in agg_dict.items():
        # Sum the specific columns for each row in the source, then groupby
        # Actually, it's more efficient to sum the columns in the source first? 
        # No, we need to group by month/hour.
        # Let's create a temporary column for the sum of these specific cols
        source[f'_sum_{col_name}'] = source[cols].sum(axis=1)
        result[col_name] = grouped[f'_sum_{col_name}'].sum().values
        
    # 5. Calculate Total
    # Total is the sum of the aggregated categories
    result['total'] = (
        result['hvac'] + 
        result['domestic_water_heating'] + 
        result['major_appliances'] + 
        result['lighting'] + 
        result['miscellaneous_plug_loads']
    )
    
    # 6. Format Output
    # Ensure types
    result['month'] = result['month'].astype(int)
    result['hour'] = result['hour'].astype(int)
    
    # Select and order columns
    final_cols = [
        'month', 
        'hour', 
        'hvac', 
        'domestic_water_heating', 
        'major_appliances', 
        'lighting', 
        'miscellaneous_plug_loads', 
        'total'
    ]
    
    result = result[final_cols]
    
    # Sort by month and hour for consistency (optional but good practice)
    result = result.sort_values(by=['month', 'hour']).reset_index(drop=True)
    
    return result
