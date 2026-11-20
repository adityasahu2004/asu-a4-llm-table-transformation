import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    ts = pd.to_datetime(source['timestamp'])
    
    # Derive season
    month = ts.dt.month
    season_map = {
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Fall', 10: 'Fall', 11: 'Fall'
    }
    out = pd.DataFrame(index=source.index)
    out['season'] = month.map(season_map)
    
    # Extract hour
    out['hour'] = ts.dt.hour.astype('int64')
    
    # Helper to get column safely
    def get_col(name):
        return source[name].astype('float64')

    # Map and aggregate columns
    # HVAC: AC Compressor + Air Handler + Minisplit
    hvac_cols = [
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    ]
    out['hvac'] = sum([get_col(c) for c in hvac_cols]).astype('int64')
    
    # Water Heating
    out['water_heating'] = get_col('WATER HEATER WHS [emon ch7,8]').astype('int64')
    
    # Refrigerator: Primary + 2nd
    fridge_cols = [
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]'
    ]
    out['refrigerator'] = sum([get_col(c) for c in fridge_cols]).astype('int64')
    
    # Clothes Washer: Wattsup Energy Washer
    out['clothes_washer'] = get_col('Wattsup Energy Washer (WHS)').astype('int64')
    
    # Clothes Dryer: 1-CT + 2-CTs
    dryer_cols = [
        'DRYER WHS (1-CT) [emon ch9]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    out['clothes_dryer'] = sum([get_col(c) for c in dryer_cols]).astype('int64')
    
    # Dishwasher
    out['dishwasher'] = get_col('DISH WASHER WHS [emon ch11]').astype('int64')
    
    # Cooking Range
    out['cooking_range'] = get_col('RANGE WHS (1-CT) [emon ch10]').astype('int64')
    
    # Pool Spa Pumps
    out['pool_spa_pumps'] = get_col('POOL PUMP WHS (2-CTs) [xpod chA-3,4]').astype('int64')
    
    # Columns with no direct source or mapped to 0 based on target distinct values
    zero_cols = [
        'interior_lighting', 'exterior_lighting', 'lighting', 
        'plug', 'pool_spa_heater'
    ]
    for col in zero_cols:
        out[col] = 0
        
    return out.reset_index(drop=True)
