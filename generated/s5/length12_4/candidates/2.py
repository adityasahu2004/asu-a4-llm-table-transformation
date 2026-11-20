import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map month to season
    def get_season(month):
        if month in ['January', 'February', 'December']:
            return 'Winter'
        elif month in ['March', 'April', 'May']:
            return 'Spring'
        elif month in ['June', 'July', 'August']:
            return 'Summer'
        elif month in ['September', 'October', 'November']:
            return 'Fall'
        return 'Unknown'
    
    source = source.copy()
    source['season'] = source['Time Period'].apply(get_season)
    source['hour'] = source['Hour Ending']
    
    # Clean demand values
    source['demand'] = pd.to_numeric(source['Average Demand Per Home With This End Use [kW]'], errors='coerce').fillna(0)
    
    # Define mapping from End Use to target columns
    # Based on the target having non-zero values only for hvac, water_heating, refrigerator, dishwasher
    # And the sample showing "Freezer", "Remaining Load", etc.
    # We assume:
    # "Remaining Load" -> hvac
    # "Freezer" -> refrigerator (or "Refrigerator" if present)
    # "Dishwasher" -> dishwasher
    # "Water Heater" -> water_heating
    
    # Identify relevant end uses. If they don't exist in source, they will just result in 0 sums.
    end_use_map = {
        'Remaining Load': 'hvac',
        'Freezer': 'refrigerator',
        'Refrigerator': 'refrigerator', # Handle potential variation
        'Dishwasher': 'dishwasher',
        'Water Heater': 'water_heating',
        'Water Heating': 'water_heating' # Handle potential variation
    }
    
    # Filter to only mapped end uses
    valid_uses = list(end_use_map.keys())
    source_filtered = source[source['End Use'].isin(valid_uses)].copy()
    
    # Map End Use to target column name
    source_filtered['target_col'] = source_filtered['End Use'].map(end_use_map)
    
    # Group by season, hour, and target_col, then sum demand
    grouped = source_filtered.groupby(['season', 'hour', 'target_col'])['demand'].sum().reset_index()
    
    # Pivot to get columns for each end use
    pivoted = grouped.pivot_table(index=['season', 'hour'], columns='target_col', values='demand', fill_value=0).reset_index()
    
    # Ensure all target columns exist, even if empty
    target_cols = ['hvac', 'water_heating', 'refrigerator', 'dishwasher']
    for col in target_cols:
        if col not in pivoted.columns:
            pivoted[col] = 0
            
    # Select and order columns
    out = pivoted[['season', 'hour'] + target_cols]
    
    # Add the constant zero columns as required by the target schema
    const_zero_cols = [
        'clothes_washer', 'clothes_dryer', 'cooking_range', 
        'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
        'lighting', 'plug', 'pool_spa_heater'
    ]
    for col in const_zero_cols:
        out[col] = 0
        
    # Reorder to match target exactly
    final_cols = ['season', 'hour', 'hvac', 'water_heating', 'refrigerator', 
                  'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 
                  'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
                  'lighting', 'plug', 'pool_spa_heater']
                  
    out = out[final_cols]
    
    # Ensure dtypes match target
    # hour is int64
    out['hour'] = out['hour'].astype(int)
    # clothes_washer, clothes_dryer, cooking_range, pool_spa_pumps, interior_lighting, exterior_lighting, lighting, plug, pool_spa_heater are int64
    int_cols = ['clothes_washer', 'clothes_dryer', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    for col in int_cols:
        out[col] = out[col].astype(int)
        
    # Sort by season and hour to ensure deterministic order? 
    # The target sample isn't strictly sorted by hour within season, but usually these are ordered.
    # The distinct count of 96 implies a full cartesian product of 4 seasons and 24 hours.
    # We should ensure all 96 rows exist.
    
    # Create a full grid of seasons and hours
    seasons = ['Winter', 'Spring', 'Summer', 'Fall']
    hours = range(1, 25)
    grid = pd.MultiIndex.from_product([seasons, hours], names=['season', 'hour'])
    full_df = pd.DataFrame(index=grid).reset_index()
    
    # Merge with our calculated data
    out = full_df.merge(out, on=['season', 'hour'], how='left')
    
    # Fill NaNs from merge with 0
    out = out.fillna(0)
    
    # Ensure dtypes again after merge
    out['hour'] = out['hour'].astype(int)
    for col in int_cols:
        out[col] = out[col].astype(int)
        
    return out
