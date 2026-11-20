import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Replace bad data flag 32767 with NaN
    df = source.replace(32767.0, np.nan)
    
    # Define aggregation groups
    hvac_cols = [
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    ]
    
    water_cols = [
        'WATER HEATER WHS [emon ch7,8]'
    ]
    
    major_cols = [
        'DRYER WHS (1-CT) [emon ch9]',
        'RANGE WHS (1-CT) [emon ch10]',
        'DISH WASHER WHS [emon ch11]',
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    
    misc_cols = [
        'Calculated Unmeasured loads (Whr)'
    ]
    
    total_cols = [
        'TOTAL BLDG WHS [emon ch1,2]'
    ]
    
    # Group by timestamp and sum
    grouped = df.groupby('timestamp').agg(
        hvac=(hvac_cols, 'sum'),
        domestic_water_heating=(water_cols, 'sum'),
        major_appliances=(major_cols, 'sum'),
        miscellaneous_plug_loads=(misc_cols, 'sum'),
        total=(total_cols, 'sum')
    ).reset_index()
    
    # Add lighting column as 0
    grouped['lighting'] = 0
    
    # Format datetime
    # The source timestamp is "YYYY-MM-DD HH:00:00"
    # The target is "YYYY-MM-DD HH:00:00"
    # We can just use the string directly or ensure format
    grouped['datetime'] = pd.to_datetime(grouped['timestamp']).dt.strftime('%Y-%m-%d %H:00:00')
    
    # Select and rename columns
    result = grouped[['datetime', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']].copy()
    
    # Cast types
    # hvac, domestic_water_heating, major_appliances, lighting, total -> int64
    # miscellaneous_plug_loads -> float64
    
    # Fill NaNs with 0 for integer columns before casting
    int_cols = ['hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'total']
    for col in int_cols:
        result[col] = result[col].fillna(0).astype('int64')
        
    result['miscellaneous_plug_loads'] = result['miscellaneous_plug_loads'].astype('float64')
    
    # Sort by datetime to match typical output expectations, though target sample order is ambiguous
    result = result.sort_values('datetime').reset_index(drop=True)
    
    return result
