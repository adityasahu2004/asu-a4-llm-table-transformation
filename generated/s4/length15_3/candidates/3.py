import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Identify numeric columns to clean
    numeric_cols = source.select_dtypes(include=[np.number]).columns.tolist()
    
    # Replace sentinel value 32767.0 with 0
    df = source.copy()
    for col in numeric_cols:
        df[col] = df[col].replace(32767.0, 0.0)
        
    # Parse timestamp
    df['timestamp_dt'] = pd.to_datetime(df['timestamp'])
    
    # Derive season
    month = df['timestamp_dt'].dt.month
    season_map = {1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring', 5: 'Spring',
                  6: 'Summer', 7: 'Summer', 8: 'Summer', 9: 'Fall', 10: 'Fall', 11: 'Fall', 12: 'Winter'}
    df['season'] = month.map(season_map)
    
    # Derive hour
    df['hour'] = df['timestamp_dt'].dt.hour
    
    # Define component columns
    hvac_cols = [
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    ]
    
    dwh_cols = [
        'WATER HEATER WHS [emon ch7,8]'
    ]
    
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
        'POOL PUMP WHS (2-CTs) [xpod chA-3,4]'
    ]
    
    total_col = 'TOTAL BLDG WHS [emon ch1,2]'
    
    # Create derived columns for summation
    df['HVAC_sum'] = df[hvac_cols].sum(axis=1)
    df['DWH_sum'] = df[dwh_cols].sum(axis=1)
    df['Major_Appl_sum'] = df[major_appl_cols].sum(axis=1)
    df['Misc_sum'] = df[misc_cols].sum(axis=1)
    df['Total_sum'] = df[total_col]
    
    # Group by season and hour
    grouped = df.groupby(['season', 'hour']).agg(
        HVAC=('HVAC_sum', 'sum'),
        domestic_water_heating=('DWH_sum', 'sum'),
        major_appliances=('Major_Appl_sum', 'sum'),
        miscellaneous_plug_loads=('Misc_sum', 'sum'),
        Total=('Total_sum', 'sum')
    ).reset_index()
    
    # Add lighting column as 0
    grouped['lighting'] = 0
    
    # Reorder columns
    result = grouped[['season', 'hour', 'HVAC', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'Total']]
    
    # Cast types
    result['HVAC'] = result['HVAC'].astype('int64')
    result['domestic_water_heating'] = result['domestic_water_heating'].astype('int64')
    result['major_appliances'] = result['major_appliances'].astype('int64')
    result['lighting'] = result['lighting'].astype('int64')
    result['miscellaneous_plug_loads'] = result['miscellaneous_plug_loads'].astype('float64')
    result['Total'] = result['Total'].astype('int64')
    
    return result
