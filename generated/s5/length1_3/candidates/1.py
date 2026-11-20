import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format the date as 'DayOfWeek MM/DD/YYYY'
    cst_formatted = dates.dt.strftime('%a %m/%d/%Y')
    
    # Define the mapping from source AM/PM columns to target 24-hour columns
    # Source order: 1AM, 2AM, ..., 11AM, 12AM(midnight), 1PM, ..., 11PM, 12PM(noon)
    # Wait, looking at source sample:
    # Cols: 1:00 AM, 2:00 AM, ..., 11:00 AM, 12:00 AM, 1:00 PM, ..., 11:00 PM, 12:00 PM
    # Standard 24h:
    # 1:00 AM -> 1:00
    # ...
    # 11:00 AM -> 11:00
    # 12:00 PM (Noon) -> 12:00
    # 1:00 PM -> 13:00
    # ...
    # 11:00 PM -> 23:00
    # 12:00 AM (Midnight) -> 24:00
    
    # Let's verify the source column names and their expected 24h equivalent
    mapping = {
        '1:00 AM': '1:00',
        '2:00 AM': '2:00',
        '3:00 AM': '3:00',
        '4:00 AM': '4:00',
        '5:00 AM': '5:00',
        '6:00 AM': '6:00',
        '7:00 AM': '7:00',
        '8:00 AM': '8:00',
        '9:00 AM': '9:00',
        '10:00 AM': '10:00',
        '11:00 AM': '11:00',
        '12:00 PM': '12:00',  # Noon
        '1:00 PM': '13:00',
        '2:00 PM': '14:00',
        '3:00 PM': '15:00',
        '4:00 PM': '16:00',
        '5:00 PM': '17:00',
        '6:00 PM': '18:00',
        '7:00 PM': '19:00',
        '8:00 PM': '20:00',
        '9:00 PM': '21:00',
        '10:00 PM': '22:00',
        '11:00 PM': '23:00',
        '12:00 AM': '24:00'  # Midnight
    }
    
    # Construct the result DataFrame
    result = pd.DataFrame()
    result['cst'] = cst_formatted
    
    for src_col, tgt_col in mapping.items():
        result[tgt_col] = source[src_col]
        
    return result.reset_index(drop=True)
