import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Filter for "All" Day Type
    df = source[source['Day Type'] == 'All'].copy()
    
    # 2. Map Time Period to Season
    season_map = {
        'December': 'Winter', 'January': 'Winter', 'February': 'Winter',
        'March': 'Spring', 'April': 'Spring', 'May': 'Spring',
        'June': 'Summer', 'July': 'Summer', 'August': 'Summer',
        'September': 'Fall', 'October': 'Fall', 'November': 'Fall'
    }
    df['season'] = df['Time Period'].map(season_map)
    
    # 3. Parse Number of Homes
    # Handle "0 (Modeled)" and other strings
    def parse_homes(val):
        if pd.isna(val):
            return 0
        val_str = str(val).strip()
        if '(Modeled)' in val_str:
            return 0
        try:
            return int(val_str)
        except ValueError:
            return 0
            
    df['num_homes'] = df['Number of Homes in Bin With This End Use Metered'].apply(parse_homes)
    
    # 4. Calculate Total Demand
    # Ensure Average Demand is numeric
    df['avg_demand'] = pd.to_numeric(df['Average Demand Per Home With This End Use [kW]'], errors='coerce')
    df['total_demand'] = df['avg_demand'] * df['num_homes']
    
    # 5. Map End Use to Target Columns
    end_use_map = {
        'Remaining Load': 'hvac',
        'Water Heater': 'water_heating',
        'Freezer': 'refrigerator',
        'Clothes Washer': 'clothes_washer',
        'Clothes Dryer - Electric': 'clothes_dryer',
        'Dishwasher': 'dishwasher',
        'Cooking Range': 'cooking_range',
        'Pool Pump': 'pool_spa_pumps',
        'Interior Lighting': 'interior_lighting',
        'Exterior Lighting': 'exterior_lighting',
        'Lighting': 'lighting',
        'Primary TV and Peripherals': 'plug',
        'Primary Desktop Computer': 'plug',
        'Misc Metered': 'plug',
        'Pool Heater': 'pool_spa_heater'
    }
    
    df['target_col'] = df['End Use'].map(end_use_map)
    
    # Drop rows where End Use doesn't map to a target column
    df = df.dropna(subset=['target_col'])
    
    # 6. Group by season, hour, and target_col, sum total_demand
    grouped = df.groupby(['season', 'Hour Ending', 'target_col'])['total_demand'].sum().reset_index()
    
    # 7. Pivot to wide format
    pivot_df = grouped.pivot_table(index=['season', 'Hour Ending'], columns='target_col', values='total_demand', fill_value=0).reset_index()
    
    # 8. Ensure all target columns exist
    target_columns = [
        'season', 'hour', 'hvac', 'water_heating', 'refrigerator', 
        'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 
        'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
        'lighting', 'plug', 'pool_spa_heater'
    ]
    
    # Rename Hour Ending to hour
    pivot_df = pivot_df.rename(columns={'Hour Ending': 'hour'})
    
    # Add missing columns with 0
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # Select and order columns
    result = pivot_df[target_columns]
    
    # 9. Cast types
    # season: str
    # hour: int64
    # hvac, water_heating, refrigerator, dishwasher: float64
    # clothes_washer, clothes_dryer, cooking_range, pool_spa_pumps, interior_lighting, exterior_lighting, lighting, plug, pool_spa_heater: int64
    
    result['season'] = result['season'].astype(str)
    result['hour'] = result['hour'].astype(int)
    
    float_cols = ['hvac', 'water_heating', 'refrigerator', 'dishwasher']
    int_cols = ['clothes_washer', 'clothes_dryer', 'cooking_range', 'pool_spa_pumps', 
                'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    
    for col in float_cols:
        result[col] = result[col].astype(float)
        
    for col in int_cols:
        result[col] = result[col].astype(int)
        
    # Sort for deterministic output (optional but good practice)
    # Target sample order is mixed, but standard is usually Season then Hour
    # We'll sort by season (Winter, Spring, Summer, Fall) and hour
    season_order = ['Winter', 'Spring', 'Summer', 'Fall']
    result['season_cat'] = pd.Categorical(result['season'], categories=season_order, ordered=True)
    result = result.sort_values(['season_cat', 'hour']).drop(columns=['season_cat']).reset_index(drop=True)
    
    return result
