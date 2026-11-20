import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    ts = pd.to_datetime(source['timestamp'])
    
    # Extract month and hour
    month = ts.dt.month.astype('int64')
    hour = ts.dt.hour.astype('int64')
    
    # Map and aggregate columns
    # HVAC: AC Compressor + Air Handler
    hvac = (source['AC COMPRESSOR WHS [emon ch3,4]'] + 
            source['AIR HANDLER WHS [emon ch5,6]'])
    
    # Water Heating
    water_heating = source['WATER HEATER WHS [emon ch7,8]']
    
    # Refrigerator: Primary + 2nd
    refrigerator = (source['Primary Fridge WHS [emon ch12]'] + 
                    source['2nd Fridge WHS [emon ch13]'])
    
    # Clothes Washer: Constant 0
    clothes_washer = pd.Series(0, index=source.index, dtype='int64')
    
    # Clothes Dryer: 1-CT + 2-CTs
    clothes_dryer = (source['DRYER WHS (1-CT) [emon ch9]'] + 
                     source['Dryer WHS (2-CTs) [xpod chA-9,10]'])
    
    # Dishwasher
    dishwasher = source['DISH WASHER WHS [emon ch11]']
    
    # Cooking Range
    cooking_range = source['RANGE WHS (1-CT) [emon ch10]']
    
    # Pool/Spa Pumps
    pool_spa_pumps = source['POOL PUMP WHS (2-CTs) [xpod chA-3,4]']
    
    # Lighting and Plug categories are constant 0
    interior_lighting = pd.Series(0, index=source.index, dtype='int64')
    exterior_lighting = pd.Series(0, index=source.index, dtype='int64')
    lighting = pd.Series(0, index=source.index, dtype='int64')
    plug = pd.Series(0, index=source.index, dtype='int64')
    pool_spa_heater = pd.Series(0, index=source.index, dtype='int64')
    
    # Construct result
    result = pd.DataFrame({
        'month': month,
        'hour': hour,
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
