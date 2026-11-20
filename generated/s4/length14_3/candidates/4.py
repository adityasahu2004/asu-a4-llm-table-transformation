import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    source['dt'] = pd.to_datetime(source['timestamp'])
    
    # Filter out invalid rows (sentinel value 32767 in total building)
    valid_mask = source['TOTAL BLDG WHS [emon ch1,2]'] != 32767
    df = source[valid_mask].copy()
    
    # Define helper to sum columns safely
    def sum_cols(col_list):
        return df[col_list].sum(axis=1).fillna(0)

    # Map columns to categories
    # HVAC: AC Compressor + Air Handler
    hvac_cols = ['AC COMPRESSOR WHS [emon ch3,4]', 'AIR HANDLER WHS [emon ch5,6]']
    df['HVAC'] = sum_cols(hvac_cols)
    
    # Domestic Water Heating
    df['domestic_water_heating'] = df['WATER HEATER WHS [emon ch7,8]'].fillna(0)
    
    # Major Appliances: Dryer(1-CT), Range, Dish Washer, Primary Fridge, 2nd Fridge
    major_appl_cols = [
        'DRYER WHS (1-CT) [emon ch9]',
        'RANGE WHS (1-CT) [emon ch10]',
        'DISH WASHER WHS [emon ch11]',
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]'
    ]
    df['major_appliances'] = sum_cols(major_appl_cols)
    
    # Lighting: Constant 0
    df['lighting'] = 0
    
    # Miscellaneous Plug Loads: Spares, Pool Pump, Minisplit, Dryer(2-CT)
    misc_cols = [
        'SPARE1 WHS (1-CT) [emon ch14]',
        'SPARE2 WHS (1-CT) [xpod chA-1]',
        'SPARE3 WHS (1-CT) [xpod chA-2]',
        'POOL PUMP WHS (2-CTs) [xpod chA-3,4]',
        'SPARE4 WHS (2-CTs) [xpod chA-5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    df['miscellaneous_plug_loads'] = sum_cols(misc_cols)
    
    # Total: Sum of all categories
    df['Total'] = df['HVAC'] + df['domestic_water_heating'] + df['major_appliances'] + df['lighting'] + df['miscellaneous_plug_loads']
    
    # Extract month and hour
    df['month'] = df['dt'].dt.month
    df['hour'] = df['dt'].dt.hour
    
    # Group by month and hour, sum the loads
    agg_dict = {
        'HVAC': 'sum',
        'domestic_water_heating': 'sum',
        'major_appliances': 'sum',
        'lighting': 'sum',
        'miscellaneous_plug_loads': 'sum',
        'Total': 'sum'
    }
    
    result = df.groupby(['month', 'hour']).agg(agg_dict).reset_index()
    
    # Ensure correct types
    result['month'] = result['month'].astype('int64')
    result['hour'] = result['hour'].astype('int64')
    result['HVAC'] = result['HVAC'].astype('int64')
    result['domestic_water_heating'] = result['domestic_water_heating'].astype('int64')
    result['major_appliances'] = result['major_appliances'].astype('int64')
    result['lighting'] = result['lighting'].astype('int64')
    result['miscellaneous_plug_loads'] = result['miscellaneous_plug_loads'].astype('float64')
    result['Total'] = result['Total'].astype('int64')
    
    # Sort to match typical output order (though not strictly required by schema, good for consistency)
    result = result.sort_values(['month', 'hour']).reset_index(drop=True)
    
    return result
