import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Format date as ISO string
    out = pd.DataFrame(index=source.index)
    out['date'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Mapping for hour columns to 12-hour format
    # Hr 1-11 -> 1:00 AM - 11:00 AM
    # Hr 12 -> 12:00 AM
    # Hr 13-23 -> 1:00 PM - 11:00 PM
    # Hr 24 -> 12:00 PM
    
    # Define the order of columns in the target
    # 1. AM hours 1-11
    # 2. 12 AM (Noon)
    # 3. PM hours 1-11
    # 4. 12 PM (Midnight)
    
    target_cols_order = []
    
    # 1:00 AM to 11:00 AM (Source Hr 1 to 11)
    for h in range(1, 12):
        target_cols_order.append(f"{h}:00 AM")
        
    # 12:00 AM (Source Hr 12)
    target_cols_order.append("12:00 AM")
    
    # 1:00 PM to 11:00 PM (Source Hr 13 to 23)
    for h in range(13, 24):
        hour_12 = h - 12
        target_cols_order.append(f"{hour_12}:00 PM")
        
    # 12:00 PM (Source Hr 24)
    target_cols_order.append("12:00 PM")
    
    # Map source columns to target columns
    for i, target_col in enumerate(target_cols_order):
        src_col = f"Hr {i + 1}"
        out[target_col] = source[src_col]
        
    return out.reset_index(drop=True)
