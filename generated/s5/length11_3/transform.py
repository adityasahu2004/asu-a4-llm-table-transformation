import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    ts = pd.to_datetime(source['timestamp'], format='%Y-%m-%d %H:%M:%S')
    month = ts.dt.month
    hour = ts.dt.hour
    
    # Map HVAC
    ac_comp = source['AC COMPRESSOR WHS [emon ch3,4]']
    air_hand = source['AIR HANDLER WHS [emon ch5,6]']
    hvac = ac_comp + air_hand
    
    # Map Water Heating
    water_heating = source['WATER HEATER WHS [emon ch7,8]']
    
    # Map Refrigerator
    fridge1 = source['Primary Fridge WHS [emon ch12]']
    fridge2 = source['2nd Fridge WHS [emon ch13]']
    refrigerator = fridge1 + fridge2
    
    # Map Clothes Dryer
    dryer1 = source['DRYER WHS (1-CT) [emon ch9]']
    dryer2 = source['Dryer WHS (2-CTs) [xpod chA-9,10]']
    clothes_dryer = dryer1 + dryer2
    
    # Map Dishwasher
    dishwasher = source['DISH WASHER WHS [emon ch11]']
    
    # Map Cooking Range
    cooking_range = source['RANGE WHS (1-CT) [emon ch10]']
    
    # Map Pool Spa Pumps
    pool_spa_pumps = source['POOL PUMP WHS (2-CTs) [xpod chA-3,4]']
    
    # Construct output DataFrame
    out = pd.DataFrame()
    out['month'] = month
    out['hour'] = hour
    out['hvac'] = hvac
    out['water_heating'] = water_heating
    out['refrigerator'] = refrigerator
    out['clothes_washer'] = 0
    out['clothes_dryer'] = clothes_dryer
    out['dishwasher'] = dishwasher
    out['cooking_range'] = cooking_range
    out['pool_spa_pumps'] = pool_spa_pumps
    out['interior_lighting'] = 0
    out['exterior_lighting'] = 0
    out['lighting'] = 0
    out['plug'] = 0
    out['pool_spa_heater'] = 0
    
    return out.reset_index(drop=True)
