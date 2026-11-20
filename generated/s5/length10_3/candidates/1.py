import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    dt = pd.to_datetime(source['timestamp'])
    
    # Helper to get column or 0 if missing (though schema implies they exist)
    def get_col(name):
        if name in source.columns:
            return source[name]
        return pd.Series(0.0, index=source.index)

    # HVAC: AC COMPRESSOR + AIR HANDLER + Minisplit
    hvac = get_col('AC COMPRESSOR WHS [emon ch3,4]') + \
           get_col('AIR HANDLER WHS [emon ch5,6]') + \
           get_col('Minisplit WHS (2-CTs) [xpod chA-7,8]')

    # Water Heating
    water_heating = get_col('WATER HEATER WHS [emon ch7,8]')

    # Refrigerator: Primary + 2nd
    refrigerator = get_col('Primary Fridge WHS [emon ch12]') + \
                   get_col('2nd Fridge WHS [emon ch13]')

    # Clothes Washer: Target is int 0. Source has cumulative/energy but no direct power.
    clothes_washer = pd.Series(0, index=source.index, dtype='int64')

    # Clothes Dryer: 1-CT + 2-CTs
    clothes_dryer = get_col('DRYER WHS (1-CT) [emon ch9]') + \
                    get_col('Dryer WHS (2-CTs) [xpod chA-9,10]')

    # Dishwasher
    dishwasher = get_col('DISH WASHER WHS [emon ch11]')

    # Cooking Range
    cooking_range = get_col('RANGE WHS (1-CT) [emon ch10]')

    # Pool Spa Pumps
    pool_spa_pumps = get_col('POOL PUMP WHS (2-CTs) [xpod chA-3,4]')

    # Lighting and Plug categories are constant 0 in target
    interior_lighting = pd.Series(0, index=source.index, dtype='int64')
    exterior_lighting = pd.Series(0, index=source.index, dtype='int64')
    lighting = pd.Series(0, index=source.index, dtype='int64')
    plug = pd.Series(0, index=source.index, dtype='int64')
    pool_spa_heater = pd.Series(0, index=source.index, dtype='int64')

    out = pd.DataFrame({
        'datetime': dt.strftime('%Y-%m-%d %H:%M:%S'),
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

    return out
