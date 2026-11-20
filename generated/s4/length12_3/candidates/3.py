import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    ts = pd.to_datetime(source['timestamp'], format='%Y-%m-%d %H:%M:%S')
    
    # Derive season
    months = ts.dt.month
    season = pd.Series('', index=source.index)
    season[months.isin([12, 1, 2])] = 'Winter'
    season[months.isin([3, 4, 5])] = 'Spring'
    season[months.isin([6, 7, 8])] = 'Summer'
    season[months.isin([9, 10, 11])] = 'Fall'
    
    # Extract hour
    hour = ts.dt.hour
    
    # Helper to get column or 0 if missing
    def get_col(name):
        if name in source.columns:
            return source[name]
        return pd.Series(0, index=source.index)

    # Map columns
    hvac = get_col('AC COMPRESSOR WHS [emon ch3,4]') + get_col('AIR HANDLER WHS [emon ch5,6]')
    water_heating = get_col('WATER HEATER WHS [emon ch7,8]')
    
    fridge1 = get_col('Primary Fridge WHS [emon ch12]')
    fridge2 = get_col('2nd Fridge WHS [emon ch13]')
    refrigerator = fridge1 + fridge2
    
    clothes_washer = pd.Series(0, index=source.index)
    
    dryer1 = get_col('DRYER WHS (1-CT) [emon ch9]')
    dryer2 = get_col('Dryer WHS (2-CTs) [xpod chA-9,10]')
    clothes_dryer = dryer1 + dryer2
    
    dishwasher = get_col('DISH WASHER WHS [emon ch11]')
    cooking_range = get_col('RANGE WHS (1-CT) [emon ch10]')
    pool_spa_pumps = get_col('POOL PUMP WHS (2-CTs) [xpod chA-3,4]')
    
    interior_lighting = pd.Series(0, index=source.index)
    exterior_lighting = pd.Series(0, index=source.index)
    lighting = pd.Series(0, index=source.index)
    plug = pd.Series(0, index=source.index)
    pool_spa_heater = pd.Series(0, index=source.index)
    
    # Construct DataFrame
    out = pd.DataFrame({
        'season': season,
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
    
    # Convert numeric columns to int64
    numeric_cols = [
        'hour', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer',
        'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps',
        'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater'
    ]
    for col in numeric_cols:
        out[col] = out[col].astype('Int64')
        
    return out
