import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    source = source.copy()
    source['dt'] = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    source['hour'] = source['dt'].dt.hour
    source['month'] = source['dt'].dt.month
    
    # Define seasons
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
            
    source['season'] = source['month'].apply(get_season)
    
    # Define column mappings
    hvac_cols = [c for c in source.columns if c.endswith('_sum') and any(k in c for k in ['air', 'furnace', 'heater', 'housefan', 'jacuzzi', 'poolpump', 'venthood', 'pool1_sum', 'pool2_sum'])]
    # Specific check for pool1/2 to avoid double counting if poolpump is separate
    # pool1_sum and pool2_sum are likely heating or general pool load. 
    # Let's include them in HVAC as they are major thermal loads.
    
    dom_water_cols = [c for c in source.columns if c.endswith('_sum') and 'waterheater' in c]
    
    major_appl_cols = [c for c in source.columns if c.endswith('_sum') and any(k in c for k in ['refrigerator', 'freezer', 'icemaker', 'oven', 'range', 'dishwasher', 'clotheswasher', 'drye', 'dryg', 'microwave'])]
    
    lighting_cols = [c for c in source.columns if c.endswith('_sum') and any(k in c for k in ['lights', 'kitchen1_sum', 'kitchen2_sum', 'livingroom', 'bedroom', 'bathroom', 'diningroom', 'garage', 'office', 'utilityroom', 'outsidelights', 'poollight', 'security', 'shed'])]
    # Remove kitchen apps from lighting if they matched 'kitchen' prefix? 
    # 'kitchenapp' contains 'kitchen'. We need to be careful.
    # Filter lighting cols to exclude apps
    lighting_cols = [c for c in lighting_cols if 'app' not in c]
    
    misc_cols = [c for c in source.columns if c.endswith('_sum') and any(k in c for k in ['kitchenapp', 'disposal', 'aquarium', 'battery', 'car', 'circpump', 'winecooler', 'wellpump', 'sewerpump', 'sumppump', 'pump1', 'sprinkler'])]
    
    # Helper to sum columns safely
    def sum_cols(cols):
        if not cols:
            return 0.0
        # Filter cols that exist in source
        valid_cols = [c for c in cols if c in source.columns]
        if not valid_cols:
            return 0.0
        return source[valid_cols].sum(axis=1, skipna=True)

    source['hvac'] = sum_cols(hvac_cols)
    source['domestic_water_heating'] = sum_cols(dom_water_cols)
    source['major_appliances'] = sum_cols(major_appl_cols)
    source['lighting'] = sum_cols(lighting_cols)
    source['miscellaneous_plug_loads'] = sum_cols(misc_cols)
    
    # Aggregate
    agg_df = source.groupby(['season', 'hour']).agg(
        hvac=('hvac', 'sum'),
        domestic_water_heating=('domestic_water_heating', 'sum'),
        major_appliances=('major_appliances', 'sum'),
        lighting=('lighting', 'sum'),
        miscellaneous_plug_loads=('miscellaneous_plug_loads', 'sum')
    ).reset_index()
    
    agg_df['total'] = agg_df[['hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads']].sum(axis=1)
    
    # Reorder columns
    result = agg_df[['season', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    return result
