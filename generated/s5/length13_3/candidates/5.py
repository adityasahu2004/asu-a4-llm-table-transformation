import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    source['timestamp_dt'] = pd.to_datetime(source['timestamp'])
    
    # Define column mappings for aggregation
    # hvac
    hvac_cols = [
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    ]
    
    # domestic_water_heating
    dwh_cols = [
        'WATER HEATER WHS [emon ch7,8]'
    ]
    
    # major_appliances
    major_appl_cols = [
        'DRYER WHS (1-CT) [emon ch9]',
        'RANGE WHS (1-CT) [emon ch10]',
        'DISH WASHER WHS [emon ch11]',
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]',
        'POOL PUMP WHS (2-CTs) [xpod chA-3,4]'
    ]
    
    # miscellaneous_plug_loads
    misc_cols = [
        'SPARE1 WHS (1-CT) [emon ch14]',
        'SPARE2 WHS (1-CT) [xpod chA-1]',
        'SPARE3 WHS (1-CT) [xpod chA-2]',
        'SPARE4 WHS (2-CTs) [xpod chA-5,6]',
        'Calculated Unmeasured loads (Whr)'
    ]
    
    # total
    total_cols = [
        'TOTAL BLDG WHS [emon ch1,2]'
    ]

    # Group by timestamp and sum
    grouped = source.groupby('timestamp_dt')
    
    # Calculate sums
    hvac_sum = grouped[hvac_cols].sum().sum(axis=1)
    dwh_sum = grouped[dwh_cols].sum().sum(axis=1)
    major_appl_sum = grouped[major_appl_cols].sum().sum(axis=1)
    misc_sum = grouped[misc_cols].sum().sum(axis=1)
    total_sum = grouped[total_cols].sum().sum(axis=1)
    
    # Create result dataframe
    result = pd.DataFrame({
        'datetime': hvac_sum.index,
        'hvac': hvac_sum.values,
        'domestic_water_heating': dwh_sum.values,
        'major_appliances': major_appl_sum.values,
        'lighting': 0,
        'miscellaneous_plug_loads': misc_sum.values,
        'total': total_sum.values
    })
    
    # Format datetime
    result['datetime'] = result['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Ensure dtypes
    result['hvac'] = result['hvac'].astype('int64')
    result['domestic_water_heating'] = result['domestic_water_heating'].astype('int64')
    result['major_appliances'] = result['major_appliances'].astype('int64')
    result['lighting'] = result['lighting'].astype('int64')
    result['miscellaneous_plug_loads'] = result['miscellaneous_plug_loads'].astype('float64')
    result['total'] = result['total'].astype('int64')
    
    return result
