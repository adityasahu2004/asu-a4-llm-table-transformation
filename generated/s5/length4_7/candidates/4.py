import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    dt = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Map hours to 12-hour format names
    # Source 1:00 -> 1:00 AM
    # Source 2:00 -> 2:00 AM
    # ...
    # Source 11:00 -> 11:00 AM
    # Source 12:00 -> 12:00 PM (Noon)
    # Source 13:00 -> 1:00 PM
    # ...
    # Source 23:00 -> 11:00 PM
    # Source 24:00:00 -> 12:00 AM (Midnight)
    
    # Define the mapping from source column to target column
    mapping = {}
    for h in range(1, 13):
        if h == 12:
            mapping[f'{h}:00'] = '12:00 PM'
        else:
            mapping[f'{h}:00'] = f'{h}:00 AM'
            
    for h in range(13, 24):
        target_h = h - 12
        mapping[f'{h}:00'] = f'{target_h}:00 PM'
        
    mapping['24:00:00'] = '12:00 AM'
    
    # Assign values
    for src_col, tgt_col in mapping.items():
        out[tgt_col] = source[src_col]
        
    # Define final column order as observed in target
    final_cols = ['date']
    # 1:00 AM to 11:00 AM
    for h in range(1, 12):
        final_cols.append(f'{h}:00 AM')
    # 12:00 AM (Midnight)
    final_cols.append('12:00 AM')
    # 1:00 PM to 11:00 PM
    for h in range(1, 12):
        final_cols.append(f'{h}:00 PM')
    # 12:00 PM (Noon)
    final_cols.append('12:00 PM')
    
    return out[final_cols].reset_index(drop=True)
