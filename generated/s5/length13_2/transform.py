import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    dt_series = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    # Round to nearest 15 minutes to normalize timestamps
    dt_series = dt_series.dt.floor('15min')
    # Format as string
    out = pd.DataFrame(index=source.index)
    out['datetime'] = dt_series.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Define column groups
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum', 'heater1_sum', 'heater2_sum', 'heater3_sum',
        'housefan1_sum', 'jacuzzi1_sum', 'pool1_sum', 'pool2_sum', 'poolpump1_sum',
        'pump1_sum', 'sprinkler1_sum', 'venthood1_sum'
    ]
    
    dwh_cols = [
        'waterheater1_sum', 'waterheater2_sum'
    ]
    
    major_appliances_cols = [
        'clotheswasher1_sum', 'clotheswasher_dryg1_sum', 'dishwasher1_sum', 'disposal1_sum',
        'drye1_sum', 'dryg1_sum', 'microwave1_sum', 'oven1_sum', 'oven2_sum', 'range1_sum',
        'refrigerator1_sum', 'refrigerator2_sum', 'winecooler1_sum'
    ]
    
    lighting_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 'lights_plugs4_sum',
        'lights_plugs5_sum', 'lights_plugs6_sum', 'livingroom1_sum', 'livingroom2_sum',
        'poollight1_sum', 'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum',
        'security1_sum', 'shed1_sum'
    ]
    
    misc_plug_cols = [
        'aquarium1_sum', 'battery1_sum', 'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum',
        'bedroom4_sum', 'bedroom5_sum', 'car1_sum', 'car2_sum', 'circpump1_sum',
        'diningroom1_sum', 'diningroom2_sum', 'garage1_sum', 'garage2_sum', 'icemaker1_sum',
        'kitchen1_sum', 'kitchen2_sum', 'kitchenapp1_sum', 'kitchenapp2_sum', 'office1_sum',
        'solar_sum', 'solar2_sum', 'sumppump1_sum', 'utilityroom1_sum', 'wellpump1_sum'
    ]
    
    # Helper to sum columns, treating NaNs as 0
    def sum_cols(cols):
        # Select columns, fill NaN with 0, sum across axis 1
        return source[cols].fillna(0).sum(axis=1)
        
    out['hvac'] = sum_cols(hvac_cols)
    out['domestic_water_heating'] = sum_cols(dwh_cols)
    out['major_appliances'] = sum_cols(major_appliances_cols)
    out['lighting'] = sum_cols(lighting_cols)
    out['miscellaneous_plug_loads'] = sum_cols(misc_plug_cols)
    out['total'] = 0
    
    return out.reset_index(drop=True)
