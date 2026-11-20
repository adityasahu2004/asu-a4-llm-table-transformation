import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the timestamp
    source = source.copy()
    source['local_15min'] = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    
    # Extract hour and month
    source['hour'] = source['local_15min'].dt.hour
    source['month'] = source['local_15min'].dt.month
    
    # Define season mapping
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
    
    # Define categories
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum',
        'heater1_sum', 'heater2_sum', 'heater3_sum',
        'housefan1_sum', 'venthood1_sum'
    ]
    
    dwh_cols = [
        'waterheater1_sum', 'waterheater2_sum'
    ]
    
    major_appliances_cols = [
        'clotheswasher1_sum', 'clotheswasher_dryg1_sum',
        'dishwasher1_sum',
        'drye1_sum', 'dryg1_sum',
        'microwave1_sum',
        'oven1_sum', 'oven2_sum',
        'range1_sum',
        'refrigerator1_sum', 'refrigerator2_sum',
        'freezer1_sum', 'icemaker1_sum', 'winecooler1_sum'
    ]
    
    lighting_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum',
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
        'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum'
    ]
    
    # Miscellaneous plug loads: all other _sum columns except grid/solar
    exclude_cols = hvac_cols + dwh_cols + major_appliances_cols + lighting_cols + ['grid_sum', 'solar_sum', 'solar2_sum']
    all_sum_cols = [c for c in source.columns if c.endswith('_sum')]
    misc_cols = [c for c in all_sum_cols if c not in exclude_cols]
    
    # Calculate category sums
    source['hvac'] = source[hvac_cols].sum(axis=1)
    source['domestic_water_heating'] = source[dwh_cols].sum(axis=1)
    source['major_appliances'] = source[major_appliances_cols].sum(axis=1)
    source['lighting'] = source[lighting_cols].sum(axis=1)
    source['miscellaneous_plug_loads'] = source[misc_cols].sum(axis=1)
    
    # Group by season and hour
    grouped = source.groupby(['season', 'hour']).agg({
        'hvac': 'sum',
        'domestic_water_heating': 'sum',
        'major_appliances': 'sum',
        'lighting': 'sum',
        'miscellaneous_plug_loads': 'sum'
    }).reset_index()
    
    # Calculate total
    grouped['total'] = (
        grouped['hvac'] + 
        grouped['domestic_water_heating'] + 
        grouped['major_appliances'] + 
        grouped['lighting'] + 
        grouped['miscellaneous_plug_loads']
    )
    
    # Sort by season and hour
    grouped = grouped.sort_values(['season', 'hour']).reset_index(drop=True)
    
    # Select and order columns
    result = grouped[['season', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    return result
