import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    dt = pd.to_datetime(source['timestamp'])
    
    # Create output dataframe
    out = pd.DataFrame()
    
    # Format datetime
    out['datetime'] = dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Map HVAC: Sum of AC Compressor, Air Handler, and Minisplit
    hvac_cols = [
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    ]
    out['hvac'] = source[hvac_cols].sum(axis=1)
    
    # Map Water Heating
    out['water_heating'] = source['WATER HEATER WHS [emon ch7,8]']
    
    # Map Refrigerator: Sum of Primary and 2nd Fridge
    fridge_cols = [
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]'
    ]
    out['refrigerator'] = source[fridge_cols].sum(axis=1)
    
    # Map Clothes Washer: Constant 0
    out['clothes_washer'] = 0
    
    # Map Clothes Dryer: Sum of 1-CT and 2-CTs Dryer
    dryer_cols = [
        'DRYER WHS (1-CT) [emon ch9]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    out['clothes_dryer'] = source[dryer_cols].sum(axis=1)
    
    # Map Dishwasher
    out['dishwasher'] = source['DISH WASHER WHS [emon ch11]']
    
    # Map Cooking Range
    out['cooking_range'] = source['RANGE WHS (1-CT) [emon ch10]']
    
    # Map Pool/Spa Pumps
    out['pool_spa_pumps'] = source['POOL PUMP WHS (2-CTs) [xpod chA-3,4]']
    
    # Map Lighting and Plug categories: Constant 0
    out['interior_lighting'] = 0
    out['exterior_lighting'] = 0
    out['lighting'] = 0
    out['plug'] = 0
    out['pool_spa_heater'] = 0
    
    # Ensure integer types for zero columns
    int_cols = ['clothes_washer', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    for col in int_cols:
        out[col] = out[col].astype('int64')
        
    return out
