import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    source['dt'] = pd.to_datetime(source['local_15min'])
    source['month'] = source['dt'].dt.month.astype(int)
    source['hour'] = source['dt'].dt.hour.astype(int)
    
    # Define column mappings for categories
    # We identify columns ending in '_sum' and map them to categories
    
    hvac_cols = [c for c in source.columns if c.endswith('_sum') and 
                 any(k in c for k in ['air', 'furnace', 'heater', 'jacuzzi', 'pool', 'pump', 'circpump', 'garage', 'housefan', 'sprinkler', 'wellpump', 'sumppump', 'sewerpump'])]
    
    domestic_water_heating_cols = [c for c in source.columns if c.endswith('_sum') and 
                                   any(k in c for k in ['waterheater'])]
    
    major_appliances_cols = [c for c in source.columns if c.endswith('_sum') and 
                             any(k in c for k in ['washer', 'dry', 'dishwasher', 'oven', 'range', 'refrigerator', 'microwave', 'icemaker', 'disposal', 'venthood', 'clotheswasher'])]
    
    lighting_cols = [c for c in source.columns if c.endswith('_sum') and 
                     any(k in c for k in ['lights', 'poollight'])]
    
    # Miscellaneous: remaining _sum columns that are not grid, solar, or already categorized
    # Exclude 'grid_sum' and 'solar_sum' and 'solar2_sum' as they are total/generation, not load categories in this context usually, 
    # but looking at the target 'total', it sums the categories. 
    # Let's look at what's left.
    all_sum_cols = [c for c in source.columns if c.endswith('_sum')]
    excluded_specific = ['grid_sum', 'solar_sum', 'solar2_sum']
    
    categorized_cols = set(hvac_cols + domestic_water_heating_cols + major_appliances_cols + lighting_cols)
    
    misc_cols = [c for c in all_sum_cols if c not in categorized_cols and c not in excluded_specific]
    
    # Create temporary columns for sums per row
    source['hvac'] = source[hvac_cols].sum(axis=1)
    source['domestic_water_heating'] = source[domestic_water_heating_cols].sum(axis=1)
    source['major_appliances'] = source[major_appliances_cols].sum(axis=1)
    source['lighting'] = source[lighting_cols].sum(axis=1)
    source['miscellaneous_plug_loads'] = source[misc_cols].sum(axis=1)
    
    # Group by month and hour
    agg_df = source.groupby(['month', 'hour']).agg({
        'hvac': 'sum',
        'domestic_water_heating': 'sum',
        'major_appliances': 'sum',
        'lighting': 'sum',
        'miscellaneous_plug_loads': 'sum'
    }).reset_index()
    
    # Calculate total
    agg_df['total'] = agg_df[['hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads']].sum(axis=1)
    
    # Select and order columns
    result = agg_df[['month', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    return result
