import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    ts = pd.to_datetime(source['timestamp'])
    
    # Derive season
    month = ts.dt.month
    season = pd.Series(np.where(month.isin([3, 4, 5]), 'Spring',
                                np.where(month.isin([6, 7, 8]), 'Summer',
                                         np.where(month.isin([9, 10, 11]), 'Fall', 'Winter'))), index=source.index)
    
    # Derive hour
    hour = ts.dt.hour.astype('int64')
    
    # Helper to safely get column, defaulting to 0 if not present
    def get_col(name):
        if name in source.columns:
            return source[name].astype(float)
        return pd.Series(0.0, index=source.index)

    # Map columns
    ac_comp = get_col('AC COMPRESSOR WHS [emon ch3,4]')
    air_hand = get_col('AIR HANDLER WHS [emon ch5,6]')
    minisplit = get_col('Minisplit WHS (2-CTs) [xpod chA-7,8]')
    
    hvac = (ac_comp + air_hand + minisplit).astype('int64')
    
    water_heating = get_col('WATER HEATER WHS [emon ch7,8]').astype('int64')
    
    fridge1 = get_col('Primary Fridge WHS [emon ch12]')
    fridge2 = get_col('2nd Fridge WHS [emon ch13]')
    refrigerator = (fridge1 + fridge2).astype('int64')
    
    # Target sample shows clothes_washer as 0. 
    # Source has 'DISH WASHER' and 'Wattsup... Washer'. 
    # Given 'dishwasher' target maps to 'DISH WASHER' source, 
    # and 'clothes_washer' target is 0, we assume 0.
    clothes_washer = pd.Series(0, index=source.index, dtype='int64')
    
    dryer1 = get_col('DRYER WHS (1-CT) [emon ch9]')
    dryer2 = get_col('Dryer WHS (2-CTs) [xpod chA-9,10]')
    clothes_dryer = (dryer1 + dryer2).astype('int64')
    
    dishwasher = get_col('DISH WASHER WHS [emon ch11]').astype('int64')
    
    cooking_range = get_col('RANGE WHS (1-CT) [emon ch10]').astype('int64')
    
    pool_pumps = get_col('POOL PUMP WHS (2-CTs) [xpod chA-3,4]').astype('int64')
    
    # Remaining targets are 0 in sample
    interior_lighting = pd.Series(0, index=source.index, dtype='int64')
    exterior_lighting = pd.Series(0, index=source.index, dtype='int64')
    lighting = pd.Series(0, index=source.index, dtype='int64')
    plug = pd.Series(0, index=source.index, dtype='int64')
    pool_spa_heater = pd.Series(0, index=source.index, dtype='int64')
    
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
        'pool_spa_pumps': pool_pumps,
        'interior_lighting': interior_lighting,
        'exterior_lighting': exterior_lighting,
        'lighting': lighting,
        'plug': plug,
        'pool_spa_heater': pool_spa_heater
    })
    
    return out.reset_index(drop=True)
