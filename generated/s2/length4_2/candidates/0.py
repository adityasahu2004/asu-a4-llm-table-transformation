import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format the date as required
    out = pd.DataFrame()
    out['date'] = dates.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Mapping for hours 1-24 to 12-hour clock format
    # value1 -> 1:00 AM
    # value12 -> 12:00 PM
    # value13 -> 1:00 PM
    # value24 -> 12:00 AM
    
    for h in range(1, 25):
        src_col = f'value{h}'
        
        if h == 12:
            tgt_col = '12:00 PM'
        elif h == 24:
            tgt_col = '12:00 AM'
        elif h < 12:
            tgt_col = f'{h}:00 AM'
        else:
            # h > 12
            tgt_col = f'{h-12}:00 PM'
            
        out[tgt_col] = source[src_col]
        
    return out
