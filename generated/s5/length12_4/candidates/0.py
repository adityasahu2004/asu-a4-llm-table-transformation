import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map months to seasons
    month_to_season = {
        'January': 'Winter', 'February': 'Winter', 'December': 'Winter',
        'March': 'Spring', 'April': 'Spring', 'May': 'Spring',
        'June': 'Summer', 'July': 'Summer', 'August': 'Summer',
        'September': 'Fall', 'October': 'Fall', 'November': 'Fall'
    }
    
    # Map End Use to target column
    end_use_map = {
        'Remaining Load': 'hvac',
        'Water Heater': 'water_heating',
        'Refrigerator': 'refrigerator',
        'Dishwasher': 'dishwasher'
    }
    
    # Filter and map
    df = source.copy()
    df['season'] = df['Time Period'].map(month_to_season)
    df['target_col'] = df['End Use'].map(end_use_map)
    
    # Keep only relevant rows
    df = df[df['target_col'].notna()].copy()
    
    # Ensure numeric
    df['val'] = pd.to_numeric(df['Average Demand Per Home With This End Use [kW]'], errors='coerce')
    
    # Group and sum
    grouped = df.groupby(['season', 'Hour Ending', 'target_col'])['val'].sum().reset_index()
    
    # Pivot to wide format
    pivoted = grouped.pivot_table(index=['season', 'Hour Ending'], columns='target_col', values='val', fill_value=0).reset_index()
    
    # Define all target columns
    all_cols = ['hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    
    # Ensure all columns exist
    for col in all_cols:
        if col not in pivoted.columns:
            pivoted[col] = 0
            
    # Select and order columns
    result = pivoted[['season', 'Hour Ending', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']]
    
    # Rename Hour Ending to hour
    result = result.rename(columns={'Hour Ending': 'hour'})
    
    # Cast integer columns to int64 as per target schema (though they are all 0)
    int_cols = ['clothes_washer', 'clothes_dryer', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    for col in int_cols:
        result[col] = result[col].astype('int64')
        
    # Cast hour to int64
    result['hour'] = result['hour'].astype('int64')
    
    # Sort for consistency (optional but good practice)
    result = result.sort_values(['season', 'hour']).reset_index(drop=True)
    
    return result
