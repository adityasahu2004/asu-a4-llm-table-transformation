import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp and format
    dt_series = pd.to_datetime(source['timestamp'])
    datetime_str = dt_series.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Map columns
    hvac = source['AC COMPRESSOR WHS [emon ch3,4]'] + source['AIR HANDLER WHS [emon ch5,6]']
    water_heating = source['WATER HEATER WHS [emon ch7,8]']
    refrigerator = source['Primary Fridge WHS [emon ch12]'] + source['2nd Fridge WHS [emon ch13]']
    clothes_washer = 0
    clothes_dryer = source['DRYER WHS (1-CT) [emon ch9]'] + source['Dryer WHS (2-CTs) [xpod chA-9,10]']
    dishwasher = source['DISH WASHER WHS [emon ch11]']
    cooking_range = source['RANGE WHS (1-CT) [emon ch10]']
    pool_spa_pumps = source['POOL PUMP WHS (2-CTs) [xpod chA-3,4]']
    
    # Constant zero columns
    interior_lighting = 0
    exterior_lighting = 0
    lighting = 0
    plug = 0
    pool_spa_heater = 0
    
    # Construct result
    result = pd.DataFrame({
        'datetime': datetime_str,
        'hvac': hvac,
        'water_heating': water_heating,
        'refrigerator': refrigerator,
        'clothes_washer': clothes_washer,
        'clothes_dryer': clothes_dryer,
        'dishwasher': dishwasher,
        'cooking_range': cooking_range,
        'pool_spa_pumps': pool_spa_pumps,
        'interior_lighting': interior_lighting,
        'exterior_lighting': exterior_lighting,
        'lighting': lighting,
        'plug': plug,
        'pool_spa_heater': pool_spa_heater
    })
    
    return result
