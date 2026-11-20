import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Replace sentinel value 32767 with NaN
    df = source.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].replace(32767.0, np.nan)

    # Define aggregation groups
    # hvac: AC Compressor + Air Handler + Minisplit
    # domestic_water_heating: Water Heater
    # major_appliances: Dryer(1-CT) + Range(1-CT) + Dish Washer + Fridge1 + Fridge2
    # lighting: 0
    # miscellaneous_plug_loads: Calculated Unmeasured loads
    # total: TOTAL BLDG WHS

    # We will group by timestamp and sum
    group_cols = ['timestamp']
    
    # Calculate components per row first to ensure correct summation logic before aggregation
    # Or just sum the columns directly in the groupby agg
    
    agg_dict = {
        'AC COMPRESSOR WHS [emon ch3,4]': 'sum',
        'AIR HANDLER WHS [emon ch5,6]': 'sum',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]': 'sum',
        'WATER HEATER WHS [emon ch7,8]': 'sum',
        'DRYER WHS (1-CT) [emon ch9]': 'sum',
        'RANGE WHS (1-CT) [emon ch10]': 'sum',
        'DISH WASHER WHS [emon ch11]': 'sum',
        'Primary Fridge WHS [emon ch12]': 'sum',
        '2nd Fridge WHS [emon ch13]': 'sum',
        'Calculated Unmeasured loads (Whr)': 'sum',
        'TOTAL BLDG WHS [emon ch1,2]': 'sum'
    }

    grouped = df.groupby('timestamp', as_index=False).agg(agg_dict)

    # Construct target columns
    out = pd.DataFrame()
    out['datetime'] = pd.to_datetime(grouped['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # HVAC
    hvac_cols = ['AC COMPRESSOR WHS [emon ch3,4]', 'AIR HANDLER WHS [emon ch5,6]', 'Minisplit WHS (2-CTs) [xpod chA-7,8]']
    out['hvac'] = grouped[hvac_cols].sum(axis=1).astype('int64')
    
    # Domestic Water Heating
    out['domestic_water_heating'] = grouped['WATER HEATER WHS [emon ch7,8]'].astype('int64')
    
    # Major Appliances
    major_cols = ['DRYER WHS (1-CT) [emon ch9]', 'RANGE WHS (1-CT) [emon ch10]', 'DISH WASHER WHS [emon ch11]', 
                  'Primary Fridge WHS [emon ch12]', '2nd Fridge WHS [emon ch13]']
    out['major_appliances'] = grouped[major_cols].sum(axis=1).astype('int64')
    
    # Lighting
    out['lighting'] = 0
    
    # Miscellaneous Plug Loads
    out['miscellaneous_plug_loads'] = grouped['Calculated Unmeasured loads (Whr)']
    
    # Total
    out['total'] = grouped['TOTAL BLDG WHS [emon ch1,2]'].astype('int64')

    return out.reset_index(drop=True)
