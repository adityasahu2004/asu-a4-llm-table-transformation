import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    # The source format is "M/D/YYYY H:MM" or "M/D/YYYY HH:MM"
    # We need to output "YYYY-MM-DD HH:MM:SS"
    dt = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    out = pd.DataFrame()
    out['datetime'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Helper to sum columns safely
    def safe_sum(cols):
        # Get columns, fillna with 0, sum across axis 1
        return source[cols].fillna(0).sum(axis=1)

    # Define groups
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum',
        'heater1_sum', 'heater2_sum', 'heater3_sum',
        'housefan1_sum'
    ]
    
    dwh_cols = [
        'waterheater1_sum', 'waterheater2_sum'
    ]
    
    major_appl_cols = [
        'refrigerator1_sum', 'refrigerator2_sum', 'freezer1_sum', 'icemaker1_sum',
        'dishwasher1_sum', 'microwave1_sum', 'oven1_sum', 'oven2_sum',
        'clotheswasher1_sum', 'drye1_sum', 'dryg1_sum', 'clotheswasher_dryg1_sum',
        'disposal1_sum', 'kitchenapp1_sum', 'kitchenapp2_sum', 'venthood1_sum'
    ]
    
    lighting_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
        'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum', 'poollight1_sum',
        'kitchen1_sum', 'kitchen2_sum',
        'livingroom1_sum', 'livingroom2_sum',
        'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
        'bathroom1_sum', 'bathroom2_sum',
        'diningroom1_sum', 'diningroom2_sum',
        'office1_sum', 'utilityroom1_sum',
        'garage1_sum', 'garage2_sum'
    ]
    
    misc_cols = [
        'car1_sum', 'car2_sum', 'jacuzzi1_sum',
        'pool1_sum', 'pool2_sum', 'poolpump1_sum',
        'sprinkler1_sum', 'security1_sum', 'shed1_sum', 'winecooler1_sum',
        'aquarium1_sum', 'battery1_sum', 'circpump1_sum',
        'sewerpump1_sum', 'sumppump1_sum', 'wellpump1_sum', 'pump1_sum'
    ]
    
    out['hvac'] = safe_sum(hvac_cols)
    out['domestic_water_heating'] = safe_sum(dwh_cols)
    out['major_appliances'] = safe_sum(major_appl_cols)
    out['lighting'] = safe_sum(lighting_cols)
    out['miscellaneous_plug_loads'] = safe_sum(misc_cols)
    
    out['total'] = 0
    
    return out.reset_index(drop=True)
