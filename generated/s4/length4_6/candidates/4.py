import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date from MM/DD/YYYY format
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Format date to YYYY-MM-DD 00:00:00
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Define the mapping from Source Hour columns to Target Names
    # Source: Hr 1 ... Hr 24
    # Target Sequence: 1:00 AM ... 11:00 AM, 12:00 AM, 1:00 PM ... 11:00 PM, 12:00 PM
    
    target_cols = []
    for h in range(1, 25):
        if h == 12:
            target_cols.append('12:00 AM')
        elif h == 24:
            target_cols.append('12:00 PM')
        else:
            # 1-11 -> AM
            # 13-23 -> PM (13->1, 14->2, etc.)
            if h < 12:
                target_cols.append(f'{h}:00 AM')
            else:
                target_cols.append(f'{h-12}:00 PM')
                
    # Rename source columns to target names
    # Source columns are 'Hr 1', 'Hr 2', ... 'Hr 24'
    source_hour_cols = [f'Hr {h}' for h in range(1, 25)]
    
    for src_col, tgt_col in zip(source_hour_cols, target_cols):
        out[tgt_col] = source[src_col]
        
    return out.reset_index(drop=True)
