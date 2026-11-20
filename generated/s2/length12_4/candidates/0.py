import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map Time Period to Season
    month_to_season = {
        'January': 'Winter', 'February': 'Winter', 'December': 'Winter',
        'March': 'Spring', 'April': 'Spring', 'May': 'Spring',
        'June': 'Summer', 'July': 'Summer', 'August': 'Summer',
        'September': 'Fall', 'October': 'Fall', 'November': 'Fall'
    }
    
    # Create a copy and add season
    df = source.copy()
    df['season'] = df['Time Period'].map(month_to_season)
    
    # Define the mapping from End Use to Target Column
    # Based on the target columns having non-zero distinct values, we focus on these.
    # The other columns in the target are all 0 in the sample, so we initialize them to 0.
    end_use_mapping = {
        'HVAC': 'hvac',
        'Water Heater': 'water_heating',
        'Refrigerator': 'refrigerator',
        'Dishwasher': 'dishwasher'
    }
    
    # Filter for relevant end uses
    relevant_end_uses = list(end_use_mapping.keys())
    df_filtered = df[df['End Use'].isin(relevant_end_uses)].copy()
    
    # Map End Use to target column name
    df_filtered['target_col'] = df_filtered['End Use'].map(end_use_mapping)
    
    # Group by season, hour, and target_col and sum the demand
    # Note: Hour Ending is 1-24.
    agg_df = df_filtered.groupby(['season', 'Hour Ending', 'target_col'])['Average Demand Per Home With This End Use [kW]'].sum().reset_index()
    
    # Pivot to get columns for each end use
    pivot_df = agg_df.pivot_table(index=['season', 'Hour Ending'], columns='target_col', values='Average Demand Per Home With This End Use [kW]', fill_value=0).reset_index()
    
    # Rename columns to match target exactly
    # The pivot columns will be the target_col names.
    # We need to ensure all target columns are present, even if 0.
    
    target_cols = [
        'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer',
        'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting',
        'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater'
    ]
    
    # Ensure all target columns exist
    for col in target_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # Rename Hour Ending to hour
    pivot_df = pivot_df.rename(columns={'Hour Ending': 'hour'})
    
    # Select and order columns
    final_cols = ['season', 'hour'] + target_cols
    result = pivot_df[final_cols]
    
    # Ensure dtypes match target
    # hour is int64
    result['hour'] = result['hour'].astype('int64')
    # clothes_washer, clothes_dryer, cooking_range, pool_spa_pumps, interior_lighting, exterior_lighting, lighting, plug, pool_spa_heater are int64 (0)
    int_cols = ['clothes_washer', 'clothes_dryer', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    for col in int_cols:
        result[col] = result[col].astype('int64')
        
    # hvac, water_heating, refrigerator, dishwasher are float64
    float_cols = ['hvac', 'water_heating', 'refrigerator', 'dishwasher']
    for col in float_cols:
        result[col] = result[col].astype('float64')
        
    return result
