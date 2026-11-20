import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    dt = pd.to_datetime(source['local_15min'])
    
    out = pd.DataFrame()
    out['datetime'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # HVAC
    out['hvac'] = (source['air1_sum'] + source['air2_sum'] + source['air3_sum'] + 
                   source['airwindowunit1_sum'] + source['housefan1_sum'] + source['venthood1_sum'])
    
    # Water Heating
    out['water_heating'] = source['waterheater1_sum'] + source['waterheater2_sum']
    
    # Refrigerator
    out['refrigerator'] = source['refrigerator1_sum'] + source['refrigerator2_sum'] + source['winecooler1_sum']
    
    # Clothes Washer
    out['clothes_washer'] = source['clotheswasher1_sum'] + source['clotheswasher_dryg1_sum']
    
    # Clothes Dryer
    out['clothes_dryer'] = source['drye1_sum'] + source['dryg1_sum']
    
    # Dishwasher
    out['dishwasher'] = source['dishwasher1_sum'] + source['disposal1_sum']
    
    # Cooking Range
    out['cooking_range'] = source['oven1_sum'] + source['oven2_sum'] + source['range1_sum'] + source['microwave1_sum']
    
    # Pool/Spa Pumps
    out['pool_spa_pumps'] = (source['poolpump1_sum'] + source['jacuzzi1_sum'] + 
                             source['pool1_sum'] + source['pool2_sum'] + source['pump1_sum'])
    
    # Interior Lighting
    interior_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 'lights_plugs4_sum', 
        'lights_plugs5_sum', 'lights_plugs6_sum', 'kitchen1_sum', 'kitchen2_sum', 
        'kitchenapp1_sum', 'kitchenapp2_sum', 'livingroom1_sum', 'livingroom2_sum', 
        'diningroom1_sum', 'diningroom2_sum', 'bedroom1_sum', 'bedroom2_sum', 
        'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum', 'bathroom1_sum', 'bathroom2_sum', 
        'office1_sum', 'utilityroom1_sum', 'shed1_sum', 'garage1_sum', 'garage2_sum'
    ]
    out['interior_lighting'] = source[interior_cols].sum(axis=1)
    
    # Exterior Lighting
    exterior_cols = ['outsidelights_plugs1_sum', 'outsidelights_plugs2_sum', 'poollight1_sum', 'sprinkler1_sum']
    out['exterior_lighting'] = source[exterior_cols].sum(axis=1)
    
    # Lighting (Interior + Exterior)
    out['lighting'] = out['interior_lighting'] + out['exterior_lighting']
    
    # Plug
    plug_cols = ['aquarium1_sum', 'battery1_sum', 'security1_sum', 'icemaker1_sum']
    out['plug'] = source[plug_cols].sum(axis=1)
    
    # Pool Spa Heater (Constant 0)
    out['pool_spa_heater'] = 0
    
    return out
