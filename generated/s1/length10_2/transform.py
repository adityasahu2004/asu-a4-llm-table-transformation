import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse and format datetime
    # Source format: "12/5/2015 17:45" -> "%m/%d/%Y %H:%M"
    # Target format: "2011-12-31 23:00:00" -> "%Y-%m-%d %H:%M:%S"
    dt_series = pd.to_datetime(source['local_15min'], format="%m/%d/%Y %H:%M")
    datetime_str = dt_series.dt.strftime("%Y-%m-%d %H:%M:%S")
    
    # 2. Define column groups for aggregation
    # HVAC: air, furnace, heater, housefan, venthood, circpump
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum',
        'heater1_sum', 'heater2_sum', 'heater3_sum',
        'housefan1_sum', 'venthood1_sum', 'circpump1_sum'
    ]
    
    # Water Heating
    water_heating_cols = [
        'waterheater1_sum', 'waterheater2_sum'
    ]
    
    # Refrigerator
    refrigerator_cols = [
        'refrigerator1_sum', 'refrigerator2_sum',
        'freezer1_sum', 'icemaker1_sum', 'winecooler1_sum'
    ]
    
    # Clothes Washer
    clothes_washer_cols = [
        'clotheswasher1_sum'
    ]
    
    # Clothes Dryer
    clothes_dryer_cols = [
        'drye1_sum', 'dryg1_sum', 'clotheswasher_dryg1_sum'
    ]
    
    # Dishwasher
    dishwasher_cols = [
        'dishwasher1_sum'
    ]
    
    # Cooking Range
    cooking_range_cols = [
        'oven1_sum', 'oven2_sum', 'range1_sum', 'microwave1_sum', 'disposal1_sum'
    ]
    
    # Pool/Spa Pumps
    pool_spa_pumps_cols = [
        'poolpump1_sum', 'jacuzzi1_sum', 'pool1_sum', 'pool2_sum'
    ]
    
    # Interior Lighting
    # Assuming lights_plugs1-6 are interior lighting
    interior_lighting_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum',
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum'
    ]
    
    # Exterior Lighting
    exterior_lighting_cols = [
        'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum', 'poollight1_sum'
    ]
    
    # Plug Loads
    # Includes battery, car, security, aquarium, and room-specific plugs/apps
    plug_cols = [
        'battery1_sum', 'car1_sum', 'car2_sum', 'security1_sum', 'aquarium1_sum',
        'kitchen1_sum', 'kitchen2_sum', 'kitchenapp1_sum', 'kitchenapp2_sum',
        'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
        'bathroom1_sum', 'bathroom2_sum',
        'livingroom1_sum', 'livingroom2_sum',
        'diningroom1_sum', 'diningroom2_sum',
        'office1_sum',
        'garage1_sum', 'garage2_sum',
        'utilityroom1_sum', 'shed1_sum',
        'sewerpump1_sum', 'sumppump1_sum', 'wellpump1_sum'
    ]

    # 3. Perform aggregations
    # Using sum(axis=1) which returns NaN if any value in the row is NaN
    df = pd.DataFrame()
    df['datetime'] = datetime_str
    df['hvac'] = source[hvac_cols].sum(axis=1)
    df['water_heating'] = source[water_heating_cols].sum(axis=1)
    df['refrigerator'] = source[refrigerator_cols].sum(axis=1)
    df['clothes_washer'] = source[clothes_washer_cols].sum(axis=1)
    df['clothes_dryer'] = source[clothes_dryer_cols].sum(axis=1)
    df['dishwasher'] = source[dishwasher_cols].sum(axis=1)
    df['cooking_range'] = source[cooking_range_cols].sum(axis=1)
    df['pool_spa_pumps'] = source[pool_spa_pumps_cols].sum(axis=1)
    df['interior_lighting'] = source[interior_lighting_cols].sum(axis=1)
    df['exterior_lighting'] = source[exterior_lighting_cols].sum(axis=1)
    df['plug'] = source[plug_cols].sum(axis=1)
    
    # Lighting is sum of interior and exterior
    # If either is NaN, lighting is NaN
    df['lighting'] = df['interior_lighting'] + df['exterior_lighting']
    
    # Pool spa heater is constant 0
    df['pool_spa_heater'] = 0
    
    # Ensure correct column order
    target_columns = [
        'datetime', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer',
        'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps',
        'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater'
    ]
    
    return df[target_columns]
