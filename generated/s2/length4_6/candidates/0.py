import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date and format it as YYYY-MM-DD 00:00:00
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    out = pd.DataFrame()
    out['date'] = dt.strftime('%Y-%m-%d 00:00:00')
    
    # Mapping from Source Hour to Target Label
    # Source Hr 1-11 -> 1:00 AM - 11:00 AM
    # Source Hr 12 -> 12:00 AM (Based on target column order position 13)
    # Source Hr 13-23 -> 1:00 PM - 11:00 PM
    # Source Hr 24 -> 12:00 PM (Based on target column order position 25)
    
    target_cols = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM',
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    source_cols = [f'Hr {i}' for i in range(1, 25)]
    
    for t_col, s_col in zip(target_cols, source_cols):
        out[t_col] = source[s_col]
        
    return out
