import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp and format as string
    dt_series = pd.to_datetime(source['timestamp'])
    datetime_str = dt_series.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Helper to safely get columns, defaulting to 0 if missing
    def get_col(name):
        if name in source.columns:
            return source[name].astype(float)
        return pd.Series(0.0, index=source.index)

    # Map columns
    hvac = (get_col('AC COMPRESSOR WHS [emon ch3,4]') + 
            get_col('AIR HANDLER WHS [emon ch5,6]') + 
            get_col('Minisplit WHS (2-CTs) [xpod chA-7,8]'))
            
    water_heating = get_col('WATER HEATER WHS [emon ch7,8]')
    
    refrigerator = (get_col('Primary Fridge WHS [emon ch12]') + 
                    get_col('2nd Fridge WHS [emon ch13]'))
    
    clothes_washer = pd.Series(0, index=source.index, dtype='int64')
    
    clothes_dryer = (get_col('DRYER WHS (1-CT) [emon ch9]') + 
                     get_col('Dryer WHS (2-CTs) [xpod chA-9,10]'))
    
    dishwasher = get_col('DISH WASHER WHS [emon ch11]')
    
    cooking_range = get_col('RANGE WHS (1-CT) [emon ch10]')
    
    pool_spa_pumps = get_col('POOL PUMP WHS (2-CTs) [xpod chA-3,4]')
    
    interior_lighting = pd.Series(0, index=source.index, dtype='int64')
    exterior_lighting = pd.Series(0, index=source.index, dtype='int64')
    lighting = pd.Series(0, index=source.index, dtype='int64')
    plug = pd.Series(0, index=source.index, dtype='int64')
    pool_spa_heater = pd.Series(0, index=source.index, dtype='int64')
    
    # Construct output DataFrame
    out = pd.DataFrame({
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
    
    return out.reset_index(drop=True)
