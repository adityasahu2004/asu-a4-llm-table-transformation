import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse and format datetime
    # The source timestamp is in "YYYY-MM-DD HH:MM:SS" format.
    # We parse it to datetime and then format it back to string to ensure consistency.
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Map and aggregate columns based on inferred relationships
    
    # HVAC: Sum of AC Compressor, Air Handler, and Minisplit
    hvac_cols = [
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    ]
    # Ensure these columns exist, if not, treat as 0
    hvac_vals = pd.DataFrame(0, index=df.index)
    for col in hvac_cols:
        if col in df.columns:
            hvac_vals += df[col]
    df['hvac'] = hvac_vals.values.astype(float)
    
    # Water Heating
    wh_col = 'WATER HEATER WHS [emon ch7,8]'
    df['water_heating'] = df[wh_col].astype(float) if wh_col in df.columns else 0.0
    
    # Refrigerator: Sum of Primary and 2nd Fridge
    fridge_cols = [
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]'
    ]
    fridge_vals = pd.DataFrame(0, index=df.index)
    for col in fridge_cols:
        if col in df.columns:
            fridge_vals += df[col]
    df['refrigerator'] = fridge_vals.values.astype(float)
    
    # Clothes Dryer: Sum of 1-CT and 2-CT Dryer columns
    dryer_cols = [
        'DRYER WHS (1-CT) [emon ch9]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    dryer_vals = pd.DataFrame(0, index=df.index)
    for col in dryer_cols:
        if col in df.columns:
            dryer_vals += df[col]
    df['clothes_dryer'] = dryer_vals.values.astype(float)
    
    # Dishwasher
    dw_col = 'DISH WASHER WHS [emon ch11]'
    df['dishwasher'] = df[dw_col].astype(float) if dw_col in df.columns else 0.0
    
    # Cooking Range
    range_col = 'RANGE WHS (1-CT) [emon ch10]'
    df['cooking_range'] = df[range_col].astype(float) if range_col in df.columns else 0.0
    
    # Pool/Spa Pumps
    pool_col = 'POOL PUMP WHS (2-CTs) [xpod chA-3,4]'
    df['pool_spa_pumps'] = df[pool_col].astype(float) if pool_col in df.columns else 0.0
    
    # Columns that are consistently 0 in the target sample
    # These are int64 in the target schema
    zero_cols = [
        'clothes_washer',
        'interior_lighting',
        'exterior_lighting',
        'lighting',
        'plug',
        'pool_spa_heater'
    ]
    for col in zero_cols:
        df[col] = 0
        
    # 3. Select and order columns as per target schema
    target_columns = [
        'datetime',
        'hvac',
        'water_heating',
        'refrigerator',
        'clothes_washer',
        'clothes_dryer',
        'dishwasher',
        'cooking_range',
        'pool_spa_pumps',
        'interior_lighting',
        'exterior_lighting',
        'lighting',
        'plug',
        'pool_spa_heater'
    ]
    
    result = df[target_columns]
    
    # Ensure dtypes match target specification
    # datetime: str
    # hvac, water_heating, refrigerator, clothes_dryer, dishwasher, cooking_range, pool_spa_pumps: float64
    # clothes_washer, interior_lighting, exterior_lighting, lighting, plug, pool_spa_heater: int64
    
    result['datetime'] = result['datetime'].astype(str)
    
    float_cols = ['hvac', 'water_heating', 'refrigerator', 'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps']
    for col in float_cols:
        result[col] = result[col].astype(float)
        
    int_cols = ['clothes_washer', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    for col in int_cols:
        result[col] = result[col].astype(int)
        
    return result
