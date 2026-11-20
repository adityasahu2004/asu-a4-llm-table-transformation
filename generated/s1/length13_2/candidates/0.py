import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse and format datetime
    # Source format: M/D/YYYY H:MM
    # Target format: YYYY-MM-DD HH:MM:SS
    source = source.copy()
    source['datetime'] = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Fill NaNs with 0 for all numeric columns to ensure sums are not NaN
    numeric_cols = source.select_dtypes(include=[np.number]).columns
    source[numeric_cols] = source[numeric_cols].fillna(0.0)
    
    # 2. Define column groups for aggregation
    
    # HVAC: Air conditioning, heating, furnaces, house fans
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum',
        'heater1_sum', 'heater2_sum', 'heater3_sum',
        'housefan1_sum'
    ]
    
    # Domestic Water Heating
    dwh_cols = [
        'waterheater1_sum', 'waterheater2_sum'
    ]
    
    # Major Appliances: Kitchen and Laundry large appliances
    major_appliances_cols = [
        'clotheswasher1_sum', 'clotheswasher_dryg1_sum',
        'dishwasher1_sum', 'drye1_sum', 'dryg1_sum',
        'microwave1_sum', 'oven1_sum', 'oven2_sum',
        'range1_sum', 'refrigerator1_sum', 'refrigerator2_sum',
        'disposal1_sum'
    ]
    
    # Lighting: Explicitly named light columns
    lighting_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum',
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
        'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum',
        'poollight1_sum'
    ]
    
    # Miscellaneous Plug Loads: Room-based loads, other specific plugs, pools, cars, etc.
    # This is the "catch-all" for non-HVAC, non-DWH, non-MajorAppliance, non-Lighting loads.
    misc_cols = [
        'kitchen1_sum', 'kitchen2_sum', 'kitchenapp1_sum', 'kitchenapp2_sum',
        'livingroom1_sum', 'livingroom2_sum',
        'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
        'bathroom1_sum', 'bathroom2_sum',
        'diningroom1_sum', 'diningroom2_sum',
        'office1_sum',
        'garage1_sum', 'garage2_sum',
        'shed1_sum',
        'utilityroom1_sum',
        'security1_sum',
        'winecooler1_sum',
        'icemaker1_sum',
        'aquarium1_sum',
        'jacuzzi1_sum',
        'pool1_sum', 'pool2_sum', 'poolpump1_sum',
        'sprinkler1_sum',
        'venthood1_sum',
        'car1_sum', 'car2_sum',
        'battery1_sum',
        'circpump1_sum',
        'pump1_sum',
        'sewerpump1_sum',
        'sumppump1_sum',
        'wellpump1_sum',
        'solar_sum', 'solar2_sum'
    ]
    
    # 3. Calculate sums
    # Using sum(axis=1) on the subset of columns
    df_result = pd.DataFrame()
    df_result['datetime'] = source['datetime']
    df_result['hvac'] = source[hvac_cols].sum(axis=1)
    df_result['domestic_water_heating'] = source[dwh_cols].sum(axis=1)
    df_result['major_appliances'] = source[major_appliances_cols].sum(axis=1)
    df_result['lighting'] = source[lighting_cols].sum(axis=1)
    df_result['miscellaneous_plug_loads'] = source[misc_cols].sum(axis=1)
    
    # 4. Add total column as 0 (int64) as per target schema
    df_result['total'] = 0
    
    # Ensure dtypes match target
    # datetime: str (already is)
    # hvac, dwh, major, lighting, misc: float64
    # total: int64
    
    df_result['hvac'] = df_result['hvac'].astype('float64')
    df_result['domestic_water_heating'] = df_result['domestic_water_heating'].astype('float64')
    df_result['major_appliances'] = df_result['major_appliances'].astype('float64')
    df_result['lighting'] = df_result['lighting'].astype('float64')
    df_result['miscellaneous_plug_loads'] = df_result['miscellaneous_plug_loads'].astype('float64')
    df_result['total'] = df_result['total'].astype('int64')
    
    return df_result
