import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=source.index)
    
    # Parse CST and format date
    dates = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    out['date'] = dates.dt.strftime('%m/%d/%Y')
    
    # Define the mapping from source hour columns to target names
    # Source columns are '1:00' through '23:00' and '24:00:00'
    # Target names follow a specific pattern
    target_names = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', 
        '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', 
        '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    for i in range(1, 25):
        src_col = f'{i}:00' if i < 24 else '24:00:00'
        tgt_col = target_names[i-1]
        out[tgt_col] = source[src_col]
        
    return out.reset_index(drop=True)
