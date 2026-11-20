import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse and Format DateTime
    # The input format is like "12/5/2015 17:45".
    # We need to parse it and format as "YYYY-MM-DD HH:MM:SS"
    dt_series = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    
    out = pd.DataFrame(index=source.index)
    out['datetime'] = dt_series.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Helper to sum columns safely (treating nulls as 0)
    def safe_sum(cols):
        # Select columns that exist, fillna with 0, sum across axis 1
        existing_cols = [c for c in cols if c in source.columns]
        if not existing_cols:
            return pd.Series(0.0, index=source.index)
        return source[existing_cols].fillna(0).sum(axis=1)

    # 2. HVAC
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'housefan1_sum', 'furnace1_sum', 'furnace2_sum',
        'heater1_sum', 'heater2_sum', 'heater3_sum',
        'venthood1_sum'
    ]
    out['hvac'] = safe_sum(hvac_cols)

    # 3. Domestic Water Heating
    water_cols = [
        'waterheater1_sum', 'waterheater2_sum', 'jacuzzi1_sum',
        'pool1_sum', 'pool2_sum', 'poolpump1_sum',
        'sumppump1_sum', 'sewerpump1_sum', 'wellpump1_sum',
        'circpump1_sum', 'pump1_sum', 'sprinkler1_sum'
    ]
    out['domestic_water_heating'] = safe_sum(water_cols)

    # 4. Major Appliances
    major_appliance_cols = [
        'refrigerator1_sum', 'refrigerator2_sum', 'freezer1_sum',
        'icemaker1_sum', 'winecooler1_sum', 'dishwasher1_sum',
        'clotheswasher1_sum', 'clotheswasher_dryg1_sum',
        'drye1_sum', 'dryg1_sum', 'oven1_sum', 'oven2_sum',
        'microwave1_sum', 'range1_sum'
    ]
    out['major_appliances'] = safe_sum(major_appliance_cols)

    # 5. Lighting
    lighting_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum',
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
        'livingroom1_sum', 'livingroom2_sum', 'kitchen1_sum', 'kitchen2_sum',
        'diningroom1_sum', 'diningroom2_sum', 'bathroom1_sum', 'bathroom2_sum',
        'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum',
        'bedroom5_sum', 'office1_sum', 'garage1_sum', 'garage2_sum',
        'shed1_sum', 'utilityroom1_sum', 'outsidelights_plugs1_sum',
        'outsidelights_plugs2_sum', 'poollight1_sum'
    ]
    out['lighting'] = safe_sum(lighting_cols)

    # 6. Miscellaneous Plug Loads
    # These are typically small electronics, chargers, etc.
    misc_cols = [
        'kitchenapp1_sum', 'kitchenapp2_sum', 'disposal1_sum',
        'aquarium1_sum', 'battery1_sum', 'car1_sum', 'car2_sum',
        'security1_sum'
    ]
    out['miscellaneous_plug_loads'] = safe_sum(misc_cols)

    # 7. Total
    out['total'] = 0

    return out.reset_index(drop=True)
