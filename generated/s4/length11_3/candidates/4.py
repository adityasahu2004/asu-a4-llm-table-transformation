import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    ts = pd.to_datetime(source['timestamp'])
    
    # Extract month and hour
    out = pd.DataFrame()
    out['month'] = ts.dt.month.astype('int64')
    out['hour'] = ts.dt.hour.astype('int64')
    
    # Map columns
    # HVAC: AC Compressor + Air Handler + Minisplit
    hvac_cols = [
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    ]
    out['hvac'] = source[hvac_cols].sum(axis=1)
    
    # Water Heating
    out['water_heating'] = source['WATER HEATER WHS [emon ch7,8]']
    
    # Refrigerator: Primary + 2nd
    fridge_cols = [
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]'
    ]
    out['refrigerator'] = source[fridge_cols].sum(axis=1)
    
    # Clothes Washer (Constant 0)
    out['clothes_washer'] = 0
    
    # Clothes Dryer: 1-CT + 2-CTs
    dryer_cols = [
        'DRYER WHS (1-CT) [emon ch9]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    out['clothes_dryer'] = source[dryer_cols].sum(axis=1)
    
    # Dishwasher
    out['dishwasher'] = source['DISH WASHER WHS [emon ch11]']
    
    # Cooking Range
    out['cooking_range'] = source['RANGE WHS (1-CT) [emon ch10]']
    
    # Pool/Spa Pumps
    out['pool_spa_pumps'] = source['POOL PUMP WHS (2-CTs) [xpod chA-3,4]']
    
    # Zero columns
    out['interior_lighting'] = 0
    out['exterior_lighting'] = 0
    out['lighting'] = 0
    out['plug'] = 0
    out['pool_spa_heater'] = 0
    
    # Ensure dtypes match target
    # Floats
    float_cols = ['hvac', 'water_heating', 'refrigerator', 'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps']
    for col in float_cols:
        out[col] = out[col].astype('float64')
        
    # Ints
    int_cols = ['month', 'hour', 'clothes_washer', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    for col in int_cols:
        out[col] = out[col].astype('int64')
        
    return out
