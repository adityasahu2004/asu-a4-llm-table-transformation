import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    ts = pd.to_datetime(source['timestamp'])
    
    # Derive hour
    hour = ts.dt.hour
    
    # Derive season
    # Winter: Dec, Jan, Feb (12, 1, 2)
    # Spring: Mar, Apr, May (3, 4, 5)
    # Summer: Jun, Jul, Aug (6, 7, 8)
    # Fall: Sep, Oct, Nov (9, 10, 11)
    month = ts.dt.month
    season = pd.Series('', index=source.index)
    season[month.isin([12, 1, 2])] = 'Winter'
    season[month.isin([3, 4, 5])] = 'Spring'
    season[month.isin([6, 7, 8])] = 'Summer'
    season[month.isin([9, 10, 11])] = 'Fall'
    
    # Map columns
    # Helper to get column safely
    def get_col(name):
        return source[name]
    
    # HVAC: AC Compressor + Air Handler
    hvac = get_col('AC COMPRESSOR WHS [emon ch3,4]') + get_col('AIR HANDLER WHS [emon ch5,6]')
    
    # Water Heating
    water_heating = get_col('WATER HEATER WHS [emon ch7,8]')
    
    # Refrigerator: Primary + 2nd
    refrigerator = get_col('Primary Fridge WHS [emon ch12]') + get_col('2nd Fridge WHS [emon ch13]')
    
    # Clothes Dryer: 1-CT + 2-CTs
    clothes_dryer = get_col('DRYER WHS (1-CT) [emon ch9]') + get_col('Dryer WHS (2-CTs) [xpod chA-9,10]')
    
    # Dishwasher
    dishwasher = get_col('DISH WASHER WHS [emon ch11]')
    
    # Cooking Range
    cooking_range = get_col('RANGE WHS (1-CT) [emon ch10]')
    
    # Pool Spa Pumps
    pool_spa_pumps = get_col('POOL PUMP WHS (2-CTs) [xpod chA-3,4]')
    
    # Zero columns
    clothes_washer = 0
    interior_lighting = 0
    exterior_lighting = 0
    lighting = 0
    plug = 0
    pool_spa_heater = 0
    
    # Construct result
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
    
    # Cast numeric columns to int64
    numeric_cols = [c for c in out.columns if c not in ['season']]
    for c in numeric_cols:
        out[c] = out[c].astype('int64')
        
    return out
