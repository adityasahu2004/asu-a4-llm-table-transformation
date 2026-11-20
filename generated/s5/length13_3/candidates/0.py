import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Replace sentinel value 32767.0 with 0
    df = source.copy()
    df = df.replace(32767.0, 0)
    
    # Parse timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Define mappings
    hvac_cols = ['AC COMPRESSOR WHS [emon ch3,4]', 'AIR HANDLER WHS [emon ch5,6]', 'Minisplit WHS (2-CTs) [xpod chA-7,8]']
    dwh_cols = ['WATER HEATER WHS [emon ch7,8]']
    major_appl_cols = [
        'DRYER WHS (1-CT) [emon ch9]', 
        'RANGE WHS (1-CT) [emon ch10]', 
        'DISH WASHER WHS [emon ch11]', 
        'Primary Fridge WHS [emon ch12]', 
        '2nd Fridge WHS [emon ch13]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    misc_cols = [
        'SPARE1 WHS (1-CT) [emon ch14]',
        'SPARE2 WHS (1-CT) [xpod chA-1]',
        'SPARE3 WHS (1-CT) [xpod chA-2]',
        'SPARE4 WHS (2-CTs) [xpod chA-5,6]',
        'Calculated Unmeasured loads (Whr)'
    ]
    total_cols = ['TOTAL BLDG WHS [emon ch1,2]']
    
    # Group by timestamp and sum
    grouped = df.groupby('timestamp').agg({
        'hvac': hvac_cols,
        'domestic_water_heating': dwh_cols,
        'major_appliances': major_appl_cols,
        'miscellaneous_plug_loads': misc_cols,
        'total': total_cols
    })
    
    # The agg above creates a multi-index columns structure if we pass lists. 
    # Better to sum the columns explicitly before grouping or use a simpler agg.
    
    # Let's create the columns first
    df['hvac'] = df[hvac_cols].sum(axis=1)
    df['domestic_water_heating'] = df[dwh_cols].sum(axis=1)
    df['major_appliances'] = df[major_appl_cols].sum(axis=1)
    df['miscellaneous_plug_loads'] = df[misc_cols].sum(axis=1)
    df['total'] = df[total_cols].sum(axis=1)
    
    # Group by timestamp and sum the aggregated columns
    result = df.groupby('timestamp').agg({
        'hvac': 'sum',
        'domestic_water_heating': 'sum',
        'major_appliances': 'sum',
        'miscellaneous_plug_loads': 'sum',
        'total': 'sum'
    }).reset_index()
    
    # Add lighting column as 0
    result['lighting'] = 0
    
    # Format datetime
    result['datetime'] = result['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Drop original timestamp
    result = result.drop(columns=['timestamp'])
    
    # Reorder columns
    result = result[['datetime', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    # Cast types
    result['hvac'] = result['hvac'].astype('int64')
    result['domestic_water_heating'] = result['domestic_water_heating'].astype('int64')
    result['major_appliances'] = result['major_appliances'].astype('int64')
    result['lighting'] = result['lighting'].astype('int64')
    result['miscellaneous_plug_loads'] = result['miscellaneous_plug_loads'].astype('float64')
    result['total'] = result['total'].astype('int64')
    
    return result
