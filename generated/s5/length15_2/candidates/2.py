import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse timestamp and extract features
    source = source.copy()
    source['local_dt'] = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    source['hour'] = source['local_dt'].dt.hour
    source['month'] = source['local_dt'].dt.month
    
    # Determine Season
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

    # 2. Define Column Groups
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum', 'housefan1_sum', 'jacuzzi1_sum',
        'poolpump1_sum', 'venthood1_sum'
    ]
    
    dwh_cols = [
        'waterheater1_sum', 'waterheater2_sum'
    ]
    
    major_appl_cols = [
        'clotheswasher1_sum', 'clotheswasher_dryg1_sum', 'dishwasher1_sum',
        'drye1_sum', 'dryg1_sum', 'microwave1_sum', 'oven1_sum', 'oven2_sum',
        'range1_sum', 'refrigerator1_sum', 'refrigerator2_sum',
        'wellpump1_sum', 'sumppump1_sum', 'sewerpump1_sum',
        'pool1_sum', 'pool2_sum'
    ]
    
    lighting_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum',
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
        'kitchen1_sum', 'kitchen2_sum', 'livingroom1_sum', 'livingroom2_sum',
        'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
        'bathroom1_sum', 'bathroom2_sum', 'diningroom1_sum', 'diningroom2_sum',
        'office1_sum', 'garage1_sum', 'garage2_sum', 'shed1_sum', 'utilityroom1_sum',
        'poollight1_sum', 'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum'
    ]
    
    misc_cols = [
        'kitchenapp1_sum', 'kitchenapp2_sum', 'disposal1_sum', 'icemaker1_sum',
        'winecooler1_sum', 'battery1_sum', 'security1_sum', 'sprinkler1_sum',
        'aquarium1_sum', 'car1_sum', 'car2_sum', 'circpump1_sum',
        'heater1_sum', 'heater2_sum', 'heater3_sum', 'pump1_sum'
    ]

    # 3. Aggregate
    # We sum the 15-minute intervals for each group
    agg_dict = {
        'hvac': (hvac_cols, 'sum'),
        'domestic_water_heating': (dwh_cols, 'sum'),
        'major_appliances': (major_appl_cols, 'sum'),
        'lighting': (lighting_cols, 'sum'),
        'miscellaneous_plug_loads': (misc_cols, 'sum')
    }
    
    # Group by season and hour
    grouped = source.groupby(['season', 'hour'])
    
    # Calculate sums for each category
    # Using apply to sum specific columns
    def sum_group(group, cols):
        return group[cols].sum().sum()

    # Construct the result dataframe
    result = grouped.apply(lambda x: pd.Series({
        'hvac': sum_group(x, hvac_cols),
        'domestic_water_heating': sum_group(x, dwh_cols),
        'major_appliances': sum_group(x, major_appl_cols),
        'lighting': sum_group(x, lighting_cols),
        'miscellaneous_plug_loads': sum_group(x, misc_cols)
    })).reset_index()

    # Calculate Total
    result['total'] = (
        result['hvac'] + 
        result['domestic_water_heating'] + 
        result['major_appliances'] + 
        result['lighting'] + 
        result['miscellaneous_plug_loads']
    )

    # Select and order columns
    result = result[['season', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    # Ensure hour is int
    result['hour'] = result['hour'].astype(int)

    return result
