import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format cst
    out = pd.DataFrame()
    out['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # Define mapping from source AM/PM columns to target 24-hour columns
    # Source columns: 1:00 AM ... 11:00 AM, 12:00 AM, 1:00 PM ... 11:00 PM, 12:00 PM
    # Target columns: 1:00 ... 24:00
    
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
        '12:00 PM': '12:00',
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
        '12:00 AM': '24:00'
    }
    
    # Apply mapping
    for src_col, tgt_col in mapping.items():
        out[tgt_col] = source[src_col]
        
    return out.reset_index(drop=True)
