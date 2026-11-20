import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    source = source.copy()
    source['local_15min'] = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    out = pd.DataFrame()
    out['datetime'] = source['local_15min'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Define helper for safe sum
    def safe_sum(*cols):
        df = source[list(cols)]
        return df.sum(axis=1, min_count=1)

    # HVAC
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum',
        'heater1_sum', 'heater2_sum', 'heater3_sum',
        'housefan1_sum', 'venthood1_sum'
    ]
    out['hvac'] = safe_sum(*hvac_cols)

    # Water Heating
    wh_cols = ['waterheater1_sum', 'waterheater2_sum']
    out['water_heating'] = safe_sum(*wh_cols)

    # Refrigerator
    ref_cols = ['refrigerator1_sum', 'refrigerator2_sum', 'freezer1_sum', 'icemaker1_sum', 'winecooler1_sum']
    out['refrigerator'] = safe_sum(*ref_cols)

    # Clothes Washer
    out['clothes_washer'] = source['clotheswasher1_sum']

    # Clothes Dryer
    dryer_cols = ['drye1_sum', 'dryg1_sum']
    out['clothes_dryer'] = safe_sum(*dryer_cols)

    # Dishwasher
    out['dishwasher'] = source['dishwasher1_sum']

    # Cooking Range
    cooking_cols = ['range1_sum', 'oven1_sum', 'oven2_sum', 'microwave1_sum']
    out['cooking_range'] = safe_sum(*cooking_cols)

    # Pool Spa Pumps
    pool_pump_cols = ['poolpump1_sum', 'jacuzzi1_sum', 'pump1_sum']
    out['pool_spa_pumps'] = safe_sum(*pool_pump_cols)

    # Interior Lighting
    int_light_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum',
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum'
    ]
    out['interior_lighting'] = safe_sum(*int_light_cols)

    # Exterior Lighting
    ext_light_cols = ['outsidelights_plugs1_sum', 'outsidelights_plugs2_sum', 'poollight1_sum']
    out['exterior_lighting'] = safe_sum(*ext_light_cols)

    # Lighting (Sum of interior and exterior)
    out['lighting'] = out['interior_lighting'] + out['exterior_lighting']

    # Plug (Remaining appliance/plug loads)
    plug_cols = [
        'kitchenapp1_sum', 'kitchenapp2_sum',
        'aquarium1_sum', 'battery1_sum',
        'car1_sum', 'car2_sum',
        'security1_sum', 'sprinkler1_sum',
        'wellpump1_sum', 'sumppump1_sum', 'sewerpump1_sum', 'circpump1_sum',
        'garage1_sum', 'garage2_sum', 'shed1_sum',
        'disposal1_sum', 'clotheswasher_dryg1_sum'
    ]
    out['plug'] = safe_sum(*plug_cols)

    # Pool Spa Heater (Constant 0 as per target schema)
    out['pool_spa_heater'] = 0

    return out
