import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp and format as required
    dt_series = pd.to_datetime(source['timestamp'])
    datetime_col = dt_series.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Map source columns to target names
    # Note: We preserve the original float values, including 32767.0 if present
    
    out = pd.DataFrame()
    out['datetime'] = datetime_col
    
    # HVAC: AC Compressor
    out['hvac'] = source['AC COMPRESSOR WHS [emon ch3,4]']
    
    # Water Heating
    out['water_heating'] = source['WATER HEATER WHS [emon ch7,8]']
    
    # Refrigerator: Primary Fridge
    out['refrigerator'] = source['Primary Fridge WHS [emon ch12]']
    
    # Clothes Washer: Constant 0 (int64)
    out['clothes_washer'] = 0
    
    # Clothes Dryer
    out['clothes_dryer'] = source['DRYER WHS (1-CT) [emon ch9]']
    
    # Dishwasher
    out['dishwasher'] = source['DISH WASHER WHS [emon ch11]']
    
    # Cooking Range
    out['cooking_range'] = source['RANGE WHS (1-CT) [emon ch10]']
    
    # Pool/Spa Pumps
    out['pool_spa_pumps'] = source['POOL PUMP WHS (2-CTs) [xpod chA-3,4]']
    
    # Interior Lighting: Constant 0 (int64)
    out['interior_lighting'] = 0
    
    # Exterior Lighting: Constant 0 (int64)
    out['exterior_lighting'] = 0
    
    # Lighting: Constant 0 (int64)
    out['lighting'] = 0
    
    # Plug: Constant 0 (int64)
    out['plug'] = 0
    
    # Pool/Spa Heater: Constant 0 (int64)
    out['pool_spa_heater'] = 0
    
    # Ensure dtypes match target specification where possible
    # The target specifies int64 for the zero columns.
    # The mapped columns are float64 in source and target.
    
    return out
