import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Derive month name
    month = dt.dt.strftime('%B')
    
    # Derive daytype: 5=Sat, 6=Sun in pandas dayofweek
    is_weekend = dt.dt.dayofweek.isin([5, 6])
    daytype = np.where(is_weekend, 'weekend', 'weekday')
    
    # Define the chronological order of source columns corresponding to hr1-hr24
    # hr1: 1:00 AM, hr2: 2:00 AM, ..., hr11: 11:00 AM
    # hr12: 12:00 PM (Noon), hr13: 1:00 PM, ..., hr24: 11:00 PM
    # Note: Source has '12:00 AM' which is Midnight (00:00). 
    # However, looking at the source sample:
    # Columns: 1:00 AM ... 11:00 AM, 12:00 AM, 1:00 PM ... 12:00 PM
    # Wait, standard 24h cycle usually starts at 00:00 or 01:00.
    # Let's look at the target sample values vs source.
    # Target hr1 = 0.401886. Source row 0 '1:00 AM' = 1.035932. 
    # Source row 0 '12:00 AM' = 0.153621.
    # The target rows do not match the source rows directly in the sample provided 
    # because the target has 183 rows and source has 182, and the values are different.
    # This implies the target is likely aggregated or from a different dataset segment, 
    # BUT the column mapping must be inferred from structure.
    
    # Standard interpretation of hourly data:
    # hr1 usually corresponds to the first hour of the day.
    # If the data is 1:00 AM to 12:00 PM, 1:00 PM to 12:00 AM?
    # Source columns:
    # 1:00 AM, 2:00 AM, 3:00 AM, 4:00 AM, 5:00 AM, 6:00 AM, 7:00 AM, 8:00 AM, 9:00 AM, 10:00 AM, 11:00 AM
    # 12:00 AM (Midnight)
    # 1:00 PM, 2:00 PM, 3:00 PM, 4:00 PM, 5:00 PM, 6:00 PM, 7:00 PM, 8:00 PM, 9:00 PM, 10:00 PM, 11:00 PM
    # 12:00 PM (Noon)
    
    # Let's assume standard chronological order for hr1-hr24:
    # hr1 = 1:00 AM
    # hr2 = 2:00 AM
    # ...
    # hr11 = 11:00 AM
    # hr12 = 12:00 PM (Noon)
    # hr13 = 1:00 PM
    # ...
    # hr23 = 11:00 PM
    # hr24 = 12:00 AM (Midnight) -- OR is hr1 12:00 AM?
    
    # Let's check the distinct counts.
    # Source '1:00 AM' distinct: 182. Target 'hr1' distinct: 183.
    # Source '12:00 AM' distinct: 182. Target 'hr24' distinct: 183.
    
    # Usually, utility data (PCT_HOURLY) starts at 1:00 AM (Hour 1) and ends at 12:00 AM (Hour 24, midnight of next day).
    # Let's map:
    # 1:00 AM -> hr1
    # 2:00 AM -> hr2
    # ...
    # 11:00 AM -> hr11
    # 12:00 PM -> hr12
    # 1:00 PM -> hr13
    # ...
    # 11:00 PM -> hr23
    # 12:00 AM -> hr24
    
    col_map = {
        '1:00 AM': 'hr1',
        '2:00 AM': 'hr2',
        '3:00 AM': 'hr3',
        '4:00 AM': 'hr4',
        '5:00 AM': 'hr5',
        '6:00 AM': 'hr6',
        '7:00 AM': 'hr7',
        '8:00 AM': 'hr8',
        '9:00 AM': 'hr9',
        '10:00 AM': 'hr10',
        '11:00 AM': 'hr11',
        '12:00 PM': 'hr12', # Noon
        '1:00 PM': 'hr13',
        '2:00 PM': 'hr14',
        '3:00 PM': 'hr15',
        '4:00 PM': 'hr16',
        '5:00 PM': 'hr17',
        '6:00 PM': 'hr18',
        '7:00 PM': 'hr19',
        '8:00 PM': 'hr20',
        '9:00 PM': 'hr21',
        '10:00 PM': 'hr22',
        '11:00 PM': 'hr23',
        '12:00 AM': 'hr24' # Midnight
    }
    
    # Select and rename columns
    hourly_cols = [source[c] for c in col_map.keys()]
    df_hourly = pd.concat(hourly_cols, axis=1)
    df_hourly.columns = col_map.values()
    
    # Construct final DataFrame
    out = pd.DataFrame({
        'month': month,
        'daytype': daytype
    })
    
    # Append hourly columns
    for col in df_hourly.columns:
        out[col] = df_hourly[col]
        
    # Ensure correct column order
    cols = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    out = out[cols]
    
    return out.reset_index(drop=True)
