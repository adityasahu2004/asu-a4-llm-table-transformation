import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map months to seasons
    month_to_season = {
        'January': 'Winter', 'February': 'Winter', 'March': 'Spring',
        'April': 'Spring', 'May': 'Spring', 'June': 'Summer',
        'July': 'Summer', 'August': 'Summer', 'September': 'Fall',
        'October': 'Fall', 'November': 'Fall', 'December': 'Winter'
    }
    
    # Filter for 'All' day type and non-null demand
    df = source[source['Day Type'] == 'All'].copy()
    df = df.dropna(subset=['Average Demand Per Home With This End Use [kW]'])
    
    # Map Time Period to season
    df['season'] = df['Time Period'].map(month_to_season)
    
    # Rename Hour Ending to hour
    df['hour'] = df['Hour Ending']
    
    # Map End Use to target columns
    end_use_map = {
        'Freezer': 'refrigerator',
        'Refrigerator': 'refrigerator',
        'Water Heater': 'water_heating',
        'HVAC': 'hvac',
        'Central Air': 'hvac',
        'Heat Pump': 'hvac',
        'Air Conditioning': 'hvac',
        'Heating': 'hvac',
        'Dishwasher': 'dishwasher',
        'Clothes Washer': 'clothes_washer',
        'Clothes Dryer - Electric': 'clothes_dryer',
        'Clothes Dryer': 'clothes_dryer',
        'Cooking Range': 'cooking_range',
        'Oven': 'cooking_range',
        'Pool Pump': 'pool_spa_pumps',
        'Spa Pump': 'pool_spa_pumps',
        'Interior Lighting': 'interior_lighting',
        'Exterior Lighting': 'exterior_lighting',
        'Lighting': 'lighting',
        'Primary TV and Peripherals': 'plug',
        'Primary Desktop Computer': 'plug',
        'TV': 'plug',
        'Computer': 'plug',
        'Pool Heater': 'pool_spa_heater',
        'Misc Metered': 'plug' # Assumption
    }
    
    df['target_col'] = df['End Use'].map(end_use_map)
    df = df.dropna(subset=['target_col']) # Drop unmapped end uses
    
    # Group and sum
    agg_df = df.groupby(['season', 'hour', 'target_col'])['Average Demand Per Home With This End Use [kW]'].sum().reset_index()
    
    # Pivot
    pivot_df = agg_df.pivot_table(index=['season', 'hour'], columns='target_col', values='Average Demand Per Home With This End Use [kW]', fill_value=0)
    
    # Define target columns
    target_cols = [
        'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer',
        'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting',
        'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater'
    ]
    
    # Reindex to ensure all columns exist
    pivot_df = pivot_df.reindex(columns=target_cols, fill_value=0)
    
    # Reset index
    pivot_df = pivot_df.reset_index()
    
    # Cast integer columns
    int_cols = ['clothes_washer', 'clothes_dryer', 'cooking_range', 'pool_spa_pumps', 
                'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    for col in int_cols:
        pivot_df[col] = pivot_df[col].astype(int)
        
    # Cast float columns
    float_cols = ['hvac', 'water_heating', 'refrigerator', 'dishwasher']
    for col in float_cols:
        pivot_df[col] = pivot_df[col].astype(float)
        
    # Ensure hour is int
    pivot_df['hour'] = pivot_df['hour'].astype(int)
    
    # Reorder columns to match target schema
    final_cols = ['season', 'hour'] + target_cols
    pivot_df = pivot_df[final_cols]
    
    return pivot_df
