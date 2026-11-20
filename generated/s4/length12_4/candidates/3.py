import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map months to seasons
    month_to_season = {
        'December': 'Winter', 'January': 'Winter', 'February': 'Winter',
        'March': 'Spring', 'April': 'Spring', 'May': 'Spring',
        'June': 'Summer', 'July': 'Summer', 'August': 'Summer',
        'September': 'Fall', 'October': 'Fall', 'November': 'Fall'
    }
    
    df = source.copy()
    
    # Assign season
    df['season'] = df['Time Period'].map(month_to_season)
    
    # Filter for 'All' day type and non-null demand
    df = df[df['Day Type'] == 'All']
    df = df.dropna(subset=['Average Demand Per Home With This End Use [kW]'])
    
    # Function to map End Use to target column name
    def map_end_use(use):
        use_lower = use.lower()
        if 'ac' in use_lower or 'cooling' in use_lower or 'heat pump' in use_lower or 'furnace' in use_lower:
            return 'hvac'
        if 'water' in use_lower:
            return 'water_heating'
        if 'refrigerator' in use_lower or 'freezer' in use_lower:
            return 'refrigerator'
        if 'dish' in use_lower:
            return 'dishwasher'
        if 'washer' in use_lower:
            return 'clothes_washer'
        if 'dryer' in use_lower:
            return 'clothes_dryer'
        if 'range' in use_lower or 'oven' in use_lower or 'cook' in use_lower:
            return 'cooking_range'
        if 'pool' in use_lower and 'pump' in use_lower:
            return 'pool_spa_pumps'
        if 'interior' in use_lower:
            return 'interior_lighting'
        if 'exterior' in use_lower:
            return 'exterior_lighting'
        if 'lighting' in use_lower:
            return 'lighting'
        if 'tv' in use_lower or 'computer' in use_lower or 'misc' in use_lower or 'plug' in use_lower:
            return 'plug'
        if 'pool' in use_lower and 'heat' in use_lower:
            return 'pool_spa_heater'
        return 'other' # Should not happen if mapping covers all 15

    df['target_col'] = df['End Use'].apply(map_end_use)
    
    # Aggregate
    agg_df = df.groupby(['season', 'Hour Ending', 'target_col'])['Average Demand Per Home With This End Use [kW]'].sum().reset_index()
    
    # Pivot
    pivot_df = agg_df.pivot_table(index=['season', 'Hour Ending'], columns='target_col', values='Average Demand Per Home With This End Use [kW]', fill_value=0)
    
    # Reset index
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns={'Hour Ending': 'hour'}, inplace=True)
    
    # Define target columns and ensure they exist
    target_cols = [
        'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer',
        'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting',
        'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater'
    ]
    
    for col in target_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # Reorder columns
    pivot_df = pivot_df[['season', 'hour'] + target_cols]
    
    # Cast dtypes as per target schema
    # Floats: hvac, water_heating, refrigerator, dishwasher
    # Ints: clothes_washer, clothes_dryer, cooking_range, pool_spa_pumps, interior_lighting, exterior_lighting, lighting, plug, pool_spa_heater
    float_cols = ['hvac', 'water_heating', 'refrigerator', 'dishwasher']
    int_cols = [c for c in target_cols if c not in float_cols]
    
    for col in float_cols:
        pivot_df[col] = pivot_df[col].astype(float)
    for col in int_cols:
        pivot_df[col] = pivot_df[col].astype(int)
        
    # Sort by season and hour? The sample isn't strictly sorted by season then hour, but it's good practice.
    # The target sample order is mixed. We'll just return the dataframe.
    # To match the exact row order of the target if necessary, we might need to sort.
    # The target sample shows: Spring, Spring, Fall, Spring, Summer, Summer, Spring, Summer, Spring, Spring, Winter, Spring.
    # It seems the target might be sorted by the original source order or just arbitrary.
    # Since we grouped, the order is determined by groupby.
    # Let's sort by season (Winter, Spring, Summer, Fall) and hour? 
    # The distinct values in target season are Spring, Fall, Summer, Winter.
    # Let's just return the grouped result.
    
    return pivot_df
