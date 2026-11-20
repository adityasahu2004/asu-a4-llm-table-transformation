import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    dt = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    source = source.copy()
    source['hour'] = dt.dt.hour
    source['month'] = dt.dt.month
    
    # Determine Season
    # Winter: Dec(12), Jan(1), Feb(2)
    # Spring: Mar(3), Apr(4), May(5)
    # Summer: Jun(6), Jul(7), Aug(8)
    # Fall: Sep(9), Oct(10), Nov(11)
    def get_season(m):
        if m in [12, 1, 2]:
            return 'Winter'
        elif m in [3, 4, 5]:
            return 'Spring'
        elif m in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
            
    source['season'] = source['month'].apply(get_season)
    
    # Define column mappings
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum', 'heater1_sum', 'heater2_sum', 'heater3_sum',
        'housefan1_sum', 'jacuzzi1_sum', 'pool1_sum', 'poolpump1_sum',
        'sprinkler1_sum', 'venthood1_sum'
    ]
    
    dwh_cols = [
        'waterheater1_sum', 'waterheater2_sum'
    ]
    
    major_appl_cols = [
        'clotheswasher1_sum', 'clotheswasher_dryg1_sum', 'dishwasher1_sum',
        'disposal1_sum', 'drye1_sum', 'dryg1_sum', 'microwave1_sum',
        'oven1_sum', 'oven2_sum', 'range1_sum', 'refrigerator1_sum',
        'refrigerator2_sum', 'freezer1_sum', 'icemaker1_sum'
    ]
    
    lighting_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum',
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
        'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum',
        'bathroom1_sum', 'bathroom2_sum', 'bedroom1_sum', 'bedroom2_sum',
        'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum', 'diningroom1_sum',
        'diningroom2_sum', 'garage1_sum', 'garage2_sum', 'kitchen1_sum',
        'kitchen2_sum', 'livingroom1_sum', 'livingroom2_sum', 'office1_sum',
        'shed1_sum', 'utilityroom1_sum', 'security1_sum', 'poollight1_sum'
    ]
    
    misc_cols = [
        'aquarium1_sum', 'battery1_sum', 'car1_sum', 'car2_sum',
        'circpump1_sum', 'kitchenapp1_sum', 'kitchenapp2_sum',
        'pump1_sum', 'sewerpump1_sum', 'sumppump1_sum', 'wellpump1_sum',
        'winecooler1_sum', 'pool2_sum'
    ]
    
    # Fill NaNs with 0 for summing purposes
    # We only care about the sum columns, so we can drop others or just select
    cols_to_keep = hvac_cols + dwh_cols + major_appl_cols + lighting_cols + misc_cols
    # Ensure all cols exist
    valid_cols = [c for c in cols_to_keep if c in source.columns]
    
    sub_df = source[['hour', 'season'] + valid_cols].copy()
    sub_df[valid_cols] = sub_df[valid_cols].fillna(0)
    
    # Calculate category sums
    sub_df['hvac'] = sub_df[hvac_cols].sum(axis=1)
    sub_df['domestic_water_heating'] = sub_df[dwh_cols].sum(axis=1)
    sub_df['major_appliances'] = sub_df[major_appl_cols].sum(axis=1)
    sub_df['lighting'] = sub_df[lighting_cols].sum(axis=1)
    sub_df['miscellaneous_plug_loads'] = sub_df[misc_cols].sum(axis=1)
    
    # Group by season and hour
    grouped = sub_df.groupby(['season', 'hour']).sum(numeric_only=True).reset_index()
    
    # Calculate total
    grouped['total'] = (grouped['hvac'] + grouped['domestic_water_heating'] + 
                        grouped['major_appliances'] + grouped['lighting'] + 
                        grouped['miscellaneous_plug_loads'])
    
    # Select final columns
    result = grouped[['season', 'hour', 'hvac', 'domestic_water_heating', 
                      'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    # Ensure hour is int
    result['hour'] = result['hour'].astype(int)
    
    return result
