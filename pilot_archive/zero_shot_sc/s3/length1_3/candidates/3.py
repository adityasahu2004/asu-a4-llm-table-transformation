import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Define mapping from source hour columns to target hour columns
    # Source: 12:00 AM, 1:00 AM, ..., 11:00 AM, 12:00 PM, ..., 11:00 PM
    # Target: 1:00,      2:00,      ..., 12:00,      13:00,     ..., 24:00
    
    mapping = {
        '12:00 AM': '1:00',
        '1:00 AM': '2:00',
        '2:00 AM': '3:00',
        '3:00 AM': '4:00',
        '4:00 AM': '5:00',
        '5:00 AM': '6:00',
        '6:00 AM': '7:00',
        '7:00 AM': '8:00',
        '8:00 AM': '9:00',
        '9:00 AM': '10:00',
        '10:00 AM': '11:00',
        '11:00 AM': '12:00',
        '12:00 PM': '13:00',
        '1:00 PM': '14:00',
        '2:00 PM': '15:00',
        '3:00 PM': '16:00',
        '4:00 PM': '17:00',
        '5:00 PM': '18:00',
        '6:00 PM': '19:00',
        '7:00 PM': '20:00',
        '8:00 PM': '21:00',
        '9:00 PM': '22:00',
        '10:00 PM': '23:00',
        '11:00 PM': '24:00'
    }
    
    # 3. Select and rename the hour columns
    hour_cols = [col for col in mapping.keys() if col in df.columns]
    df_renamed = df[['parsed_date'] + hour_cols].copy()
    df_renamed.rename(columns=mapping, inplace=True)
    
    # 4. Format the date column to match target 'cst' format
    # Target format: "Wed 01/01/2014" -> %a %m/%d/%Y
    df_renamed['cst'] = df_renamed['parsed_date'].dt.strftime('%a %m/%d/%Y')
    
    # 5. Select final columns in the correct order
    # Target columns: cst, 1:00, 2:00, ..., 24:00
    target_hour_cols = [f'{h}:00' for h in range(1, 25)]
    final_cols = ['cst'] + target_hour_cols
    
    result = df_renamed[final_cols].copy()
    
    # 6. Ensure numeric types for hour columns
    for col in target_hour_cols:
        result[col] = pd.to_numeric(result[col], errors='coerce')
        
    # 7. Sort by date to match the likely order in target (ascending date)
    # We sort by the parsed date to ensure chronological order, then drop the helper column
    result['parsed_date'] = df_renamed['parsed_date'].values
    result = result.sort_values('parsed_date').reset_index(drop=True)
    result = result.drop(columns=['parsed_date'])
    
    return result
