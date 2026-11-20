import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp to extract month and hour
    ts = pd.to_datetime(source['timestamp'])
    out = pd.DataFrame()
    out['month'] = ts.dt.month.astype('int64')
    out['hour'] = ts.dt.hour.astype('int64')
    
    # Define column mappings for summation
    # hvac: AC Compressor + Air Handler + Minisplit
    col_ac = 'AC COMPRESSOR WHS [emon ch3,4]'
    col_air = 'AIR HANDLER WHS [emon ch5,6]'
    col_mini = 'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    
    # water_heating
    col_wh = 'WATER HEATER WHS [emon ch7,8]'
    
    # refrigerator: Primary + 2nd
    col_fridge1 = 'Primary Fridge WHS [emon ch12]'
    col_fridge2 = '2nd Fridge WHS [emon ch13]'
    
    # clothes_dryer: Dryer 1-CT + Dryer 2-CTs
    col_dryer1 = 'DRYER WHS (1-CT) [emon ch9]'
    col_dryer2 = 'Dryer WHS (2-CTs) [xpod chA-9,10]'
    
    # dishwasher
    col_dw = 'DISH WASHER WHS [emon ch11]'
    
    # cooking_range
    col_range = 'RANGE WHS (1-CT) [emon ch10]'
    
    # pool_spa_pumps
    col_pool = 'POOL PUMP WHS (2-CTs) [xpod chA-3,4]'
    
    # Perform calculations
    # Note: Preserving 32767 as per target sample appearance, simple arithmetic sum
    out['hvac'] = (source[col_ac] + source[col_air] + source[col_mini]).astype('float64')
    out['water_heating'] = source[col_wh].astype('float64')
    out['refrigerator'] = (source[col_fridge1] + source[col_fridge2]).astype('float64')
    out['clothes_dryer'] = (source[col_dryer1] + source[col_dryer2]).astype('float64')
    out['dishwasher'] = source[col_dw].astype('float64')
    out['cooking_range'] = source[col_range].astype('float64')
    out['pool_spa_pumps'] = source[col_pool].astype('float64')
    
    # Constant zero columns as int64
    out['clothes_washer'] = 0
    out['interior_lighting'] = 0
    out['exterior_lighting'] = 0
    out['lighting'] = 0
    out['plug'] = 0
    out['pool_spa_heater'] = 0
    
    # Ensure dtypes match target
    out['clothes_washer'] = out['clothes_washer'].astype('int64')
    out['interior_lighting'] = out['interior_lighting'].astype('int64')
    out['exterior_lighting'] = out['exterior_lighting'].astype('int64')
    out['lighting'] = out['lighting'].astype('int64')
    out['plug'] = out['plug'].astype('int64')
    out['pool_spa_heater'] = out['pool_spa_heater'].astype('int64')
    
    # Reorder columns to match target schema
    target_cols = [
        'month', 'hour', 'hvac', 'water_heating', 'refrigerator', 
        'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 
        'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
        'lighting', 'plug', 'pool_spa_heater'
    ]
    
    return out[target_cols]
