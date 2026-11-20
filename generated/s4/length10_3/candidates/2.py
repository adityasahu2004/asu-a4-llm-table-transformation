import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    dt = pd.to_datetime(source['timestamp'])
    out = pd.DataFrame()
    out['datetime'] = dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Define column mappings
    # hvac: AC Compressor + Air Handler + Minisplit
    hvac_cols = [
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    ]
    out['hvac'] = source[hvac_cols].sum(axis=1)
    
    # water_heating: Water Heater
    out['water_heating'] = source['WATER HEATER WHS [emon ch7,8]']
    
    # refrigerator: Primary Fridge + 2nd Fridge
    fridge_cols = [
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]'
    ]
    out['refrigerator'] = source[fridge_cols].sum(axis=1)
    
    # clothes_washer: Not clearly mapped, default to 0
    out['clothes_washer'] = 0
    
    # clothes_dryer: Dryer (1-CT) + Dryer (2-CTs)
    dryer_cols = [
        'DRYER WHS (1-CT) [emon ch9]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    out['clothes_dryer'] = source[dryer_cols].sum(axis=1)
    
    # dishwasher: Dish Washer
    out['dishwasher'] = source['DISH WASHER WHS [emon ch11]']
    
    # cooking_range: Range
    out['cooking_range'] = source['RANGE WHS (1-CT) [emon ch10]']
    
    # pool_spa_pumps: Pool Pump
    out['pool_spa_pumps'] = source['POOL PUMP WHS (2-CTs) [xpod chA-3,4]']
    
    # interior_lighting: Default to 0
    out['interior_lighting'] = 0
    
    # exterior_lighting: Default to 0
    out['exterior_lighting'] = 0
    
    # lighting: Default to 0
    out['lighting'] = 0
    
    # plug: Default to 0
    out['plug'] = 0
    
    # pool_spa_heater: Default to 0
    out['pool_spa_heater'] = 0
    
    # Ensure dtypes match target
    # float64
    float_cols = ['hvac', 'water_heating', 'refrigerator', 'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps']
    for col in float_cols:
        out[col] = out[col].astype('float64')
        
    # int64
    int_cols = ['clothes_washer', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    for col in int_cols:
        out[col] = out[col].astype('int64')
        
    return out
