import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format as 'DayOfWeek MM/DD/YYYY'
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    out['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # Define mapping from source AM/PM columns to target 24h columns
    # Source order: 1-11 AM, 12 AM, 1-11 PM, 12 PM
    # Target order: 1-24 (where 24:00 is midnight/end of day)
    
    # 1:00 AM to 11:00 AM -> 1:00 to 11:00
    for h in range(1, 12):
        out[f'{h}:00'] = source[f'{h}:00 AM']
        
    # 12:00 PM -> 12:00
    out['12:00'] = source['12:00 PM']
    
    # 1:00 PM to 11:00 PM -> 13:00 to 23:00
    for h in range(1, 12):
        out[f'{h+12}:00'] = source[f'{h}:00 PM']
        
    # 12:00 AM -> 24:00
    out['24:00'] = source['12:00 AM']
    
    return out.reset_index(drop=True)
