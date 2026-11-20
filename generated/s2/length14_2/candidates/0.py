import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the timestamp
    # The format varies slightly in sample: "12/5/2015 17:45", "4/14/2016 4:15"
    # pd.to_datetime handles this automatically
    source['dt'] = pd.to_datetime(source['local_15min'])
    source['month'] = source['dt'].dt.month
    source['hour'] = source['dt'].dt.hour
    
    # Define category mappings
    # We identify columns ending in '_sum'
    sum_cols = [c for c in source.columns if c.endswith('_sum')]
    
    # Initialize category columns with 0
    categories = ['hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads']
    for cat in categories:
        source[cat] = 0.0
        
    # Mapping logic
    hvac_keywords = ['air', 'furnace', 'heater', 'ac', 'cool', 'heat', 'venthood', 'housefan']
    dwh_keywords = ['waterheater']
    major_appliance_keywords = ['oven', 'dishwasher', 'clotheswasher', 'drye', 'dryg', 'refrigerator', 'freezer', 'icemaker', 'microwave', 'range']
    lighting_keywords = ['lights', 'poollight']
    
    # Miscellaneous plug loads are everything else that is a load (not generation/grid)
    # Generation/Grid keywords to exclude
    exclude_keywords = ['grid', 'solar']
    
    for col in sum_cols:
        col_lower = col.lower()
        
        # Check if it should be excluded (generation/grid)
        is_excluded = False
        for kw in exclude_keywords:
            if kw in col_lower:
                is_excluded = True
                break
        
        if is_excluded:
            continue
            
        # Determine category
        assigned = False
        
        # HVAC
        for kw in hvac_keywords:
            if kw in col_lower:
                source['hvac'] += source[col]
                assigned = True
                break
        
        if assigned:
            continue
            
        # Domestic Water Heating
        for kw in dwh_keywords:
            if kw in col_lower:
                source['domestic_water_heating'] += source[col]
                assigned = True
                break
                
        if assigned:
            continue
            
        # Major Appliances
        for kw in major_appliance_keywords:
            if kw in col_lower:
                source['major_appliances'] += source[col]
                assigned = True
                break
                
        if assigned:
            continue
            
        # Lighting
        for kw in lighting_keywords:
            if kw in col_lower:
                source['lighting'] += source[col]
                assigned = True
                break
                
        if assigned:
            continue
            
        # Miscellaneous Plug Loads (default for remaining loads)
        source['miscellaneous_plug_loads'] += source[col]

    # Group by month and hour, summing the categories
    agg_df = source.groupby(['month', 'hour'])[categories].sum().reset_index()
    
    # Calculate total
    agg_df['total'] = agg_df[categories].sum(axis=1)
    
    # Select and order columns
    result = agg_df[['month', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    # Ensure types
    result['month'] = result['month'].astype('int64')
    result['hour'] = result['hour'].astype('int64')
    
    return result
