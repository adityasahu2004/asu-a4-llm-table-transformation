import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # 2. Create dt_strata in M/D/YYYY format
    dt_strata = dt.dt.strftime('%-m/%-d/%Y')
    
    # 3. Calculate dow (Monday=0, Sunday=6)
    dow = dt.dt.dayofweek
    
    # 4. Map source columns to target hourly columns
    # Source columns order for 1-12 AM/PM mapping:
    # 1:00 AM, 2:00 AM, ..., 11:00 AM, 12:00 PM, 1:00 PM, ..., 11:00 PM, 12:00 AM
    
    # Define the mapping from target hour index (1-24) to source column name
    # Hours 1-11 are AM (1:00 AM to 11:00 AM)
    # Hour 12 is 12:00 PM
    # Hours 13-23 are PM (1:00 PM to 11:00 PM)
    # Hour 24 is 12:00 AM
    
    cols_map = {
        1: '1:00 AM',
        2: '2:00 AM',
        3: '3:00 AM',
        4: '4:00 AM',
        5: '5:00 AM',
        6: '6:00 AM',
        7: '7:00 AM',
        8: '8:00 AM',
        9: '9:00 AM',
        10: '10:00 AM',
        11: '11:00 AM',
        12: '12:00 PM',
        13: '1:00 PM',
        14: '2:00 PM',
        15: '3:00 PM',
        16: '4:00 PM',
        17: '5:00 PM',
        18: '6:00 PM',
        19: '7:00 PM',
        20: '8:00 PM',
        21: '9:00 PM',
        22: '10:00 PM',
        23: '11:00 PM',
        24: '12:00 AM'
    }
    
    # Build the result dataframe
    res = pd.DataFrame()
    res['dt_strata'] = dt_strata
    res['dow'] = dow
    
    for h in range(1, 25):
        src_col = cols_map[h]
        res[f'pct_hourly_{h:02d}00'] = source[src_col]
        
    # 5. Append the constant 25th hour column
    res['pct_hourly_2500'] = 0
    
    return res
