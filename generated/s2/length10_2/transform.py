import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    dt = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    
    out = pd.DataFrame(index=source.index)
    out['datetime'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Helper to sum columns safely
    def safe_sum(*cols):
        # Select only existing columns to avoid KeyError if schema varies slightly
        existing_cols = [c for c in cols if c in source.columns]
        if not existing_cols:
            return pd.Series(np.nan, index=source.index)
        # Sum axis=1, skipna=True handles NaNs in individual cells
        return source[existing_cols].sum(axis=1, skipna=True)

    # HVAC
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum', 'housefan1_sum', 'venthood1_sum'
    ]
    out['hvac'] = safe_sum(*hvac_cols)

    # Water Heating
    wh_cols = ['waterheater1_sum', 'waterheater2_sum']
    out['water_heating'] = safe_sum(*wh_cols)

    # Refrigerator
    ref_cols = ['refrigerator1_sum', 'refrigerator2_sum', 'freezer1_sum', 'icemaker1_sum', 'winecooler1_sum']
    out['refrigerator'] = safe_sum(*ref_cols)

    # Clothes Washer
    out['clothes_washer'] = source.get('clotheswasher1_sum', pd.Series(np.nan, index=source.index))

    # Clothes Dryer
    cd_cols = ['drye1_sum', 'dryg1_sum', 'clotheswasher_dryg1_sum']
    out['clothes_dryer'] = safe_sum(*cd_cols)

    # Dishwasher
    out['dishwasher'] = source.get('dishwasher1_sum', pd.Series(np.nan, index=source.index))

    # Cooking Range
    cr_cols = ['oven1_sum', 'oven2_sum', 'range1_sum', 'microwave1_sum', 'disposal1_sum']
    out['cooking_range'] = safe_sum(*cr_cols)

    # Pool/Spa Pumps
    psp_cols = [
        'poolpump1_sum', 'jacuzzi1_sum', 'pool1_sum', 'pool2_sum',
        'pump1_sum', 'sumppump1_sum', 'sewerpump1_sum', 'wellpump1_sum', 'circpump1_sum'
    ]
    out['pool_spa_pumps'] = safe_sum(*psp_cols)

    # Interior Lighting
    il_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 'lights_plugs4_sum',
        'lights_plugs5_sum', 'lights_plugs6_sum',
        'kitchen1_sum', 'kitchen2_sum',
        'livingroom1_sum', 'livingroom2_sum',
        'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
        'bathroom1_sum', 'bathroom2_sum',
        'diningroom1_sum', 'diningroom2_sum',
        'office1_sum', 'utilityroom1_sum',
        'garage1_sum', 'garage2_sum', 'shed1_sum'
    ]
    out['interior_lighting'] = safe_sum(*il_cols)

    # Exterior Lighting
    el_cols = ['outsidelights_plugs1_sum', 'outsidelights_plugs2_sum', 'poollight1_sum', 'sprinkler1_sum']
    out['exterior_lighting'] = safe_sum(*el_cols)

    # Lighting (Interior + Exterior)
    out['lighting'] = out['interior_lighting'] + out['exterior_lighting']

    # Plug Loads
    plug_cols = [
        'kitchenapp1_sum', 'kitchenapp2_sum',
        'aquarium1_sum', 'battery1_sum',
        'car1_sum', 'car2_sum',
        'security1_sum',
        'heater1_sum', 'heater2_sum', 'heater3_sum'
    ]
    out['plug'] = safe_sum(*plug_cols)

    # Pool Spa Heater (Constant 0)
    out['pool_spa_heater'] = 0

    return out.reset_index(drop=True)
