import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date from CST column
    # Format: "Sat 12/01/2012" -> %a %m/%d/%Y
    dt = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    # Create date column in MM/DD/YYYY format
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Define the mapping from source hour columns to target hour columns
    # Source: 1:00 to 24:00:00
    # Target: 1:00 AM ... 11:00 AM, 12:00 AM, 1:00 PM ... 11:00 PM, 12:00 PM
    
    # Helper to get source column name
    def get_src_col(h):
        if h == 24:
            return '24:00:00'
        return f'{h}:00'
        
    # Helper to get target column name
    def get_tgt_col(h):
        if h == 12:
            return '12:00 AM'
        if h == 24:
            return '12:00 PM'
        
        h_12 = h % 12
        if h_12 == 0:
            h_12 = 12
            
        if h < 12:
            return f'{h_12}:00 AM'
        else:
            return f'{h_12}:00 PM'

    # The target order is specific:
    # 1AM, 2AM, ..., 11AM, 12AM, 1PM, ..., 11PM, 12PM
    # This corresponds to source hours:
    # 1, 2, ..., 11, 12, 13, ..., 23, 24
    
    target_order_hours = list(range(1, 12)) + [12] + list(range(13, 24)) + [24]
    
    for h in target_order_hours:
        src_col = get_src_col(h)
        tgt_col = get_tgt_col(h)
        out[tgt_col] = source[src_col].values
        
    return out.reset_index(drop=True)
