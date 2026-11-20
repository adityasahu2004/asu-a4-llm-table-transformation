import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse time
    source['time_dt'] = pd.to_datetime(source['time'])
    
    # Define season
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
            
    source['season'] = source['time_dt'].dt.month.apply(get_season)
    source['hour'] = source['time_dt'].dt.hour
    
    # Calculate weight
    source['weight'] = source['scaled_unit_count'] / source['raw_count']
    
    # Define HVAC columns
    hvac_cols = [
        'electricity_cooling_kwh',
        'electricity_central_system_cooling_kwh',
        'electricity_heating_kwh',
        'electricity_central_system_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_pumps_cooling_kwh',
        'electricity_central_system_pumps_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_central_system_pumps_heating_kwh'
    ]
    
    # Define other mappings
    mappings = {
        'water_heating': ['electricity_water_systems_kwh'],
        'refrigerator': ['electricity_refrigerator_kwh'],
        'clothes_washer': ['electricity_clothes_washer_kwh'],
        'clothes_dryer': ['electricity_clothes_dryer_kwh'],
        'dishwasher': ['electricity_dishwasher_kwh'],
        'cooking_range': ['electricity_cooking_range_kwh'],
        'pool_spa_pumps': ['electricity_pool_pump_kwh', 'electricity_hot_tub_pump_kwh'],
        'interior_lighting': ['electricity_interior_lighting_kwh'],
        'exterior_lighting': ['electricity_exterior_lighting_kwh'],
        'plug': ['electricity_plug_loads_kwh'],
        'pool_spa_heaters': ['electricity_pool_heater_kwh', 'electricity_hot_tub_heater_kwh']
    }
    
    # Create weighted columns
    for col in source.columns:
        if col in hvac_cols or any(col in v for v in mappings.values()):
            source[f'w_{col}'] = source[col] * source['weight']
            
    # Group and sum
    group_cols = ['season', 'hour']
    
    # Aggregate HVAC
    agg_dict = {}
    agg_dict['hvac'] = (pd.concat([source[f'w_{c}'] for c in hvac_cols], axis=1).sum(axis=1), 'sum')
    
    for name, cols in mappings.items():
        agg_dict[name] = (pd.concat([source[f'w_{c}'] for c in cols], axis=1).sum(axis=1), 'sum')
        
    # We need to group by season and hour. 
    # Since we have custom aggregations, let's do it manually or use agg with custom functions?
    # Easier: Create a dataframe with just the grouped keys and the summed weighted values.
    
    temp_df = source[group_cols + ['weight']].copy() # weight is scalar per row, but we need to sum weighted values
    
    # Let's create a single row per source row with all weighted sums
    weighted_df = source[group_cols].copy()
    weighted_df['hvac'] = pd.concat([source[f'w_{c}'] for c in hvac_cols], axis=1).sum(axis=1)
    
    for name, cols in mappings.items():
        weighted_df[name] = pd.concat([source[f'w_{c}'] for c in cols], axis=1).sum(axis=1)
        
    # Group and sum
    result = weighted_df.groupby(group_cols, as_index=False).sum()
    
    # Add lighting
    result['lighting'] = result['interior_lighting'] + result['exterior_lighting']
    
    # Select and order columns
    cols = [
        'season', 'hour', 'hvac', 'water_heating', 'refrigerator', 
        'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range',
        'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting',
        'plug', 'pool_spa_heaters'
    ]
    
    return result[cols].reset_index(drop=True)
