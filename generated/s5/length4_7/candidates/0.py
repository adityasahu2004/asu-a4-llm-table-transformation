import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date string "Thu 10/01/2009" to datetime
    dt_series = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Format date as MM/DD/YYYY
    out = pd.DataFrame()
    out['date'] = dt_series.dt.strftime('%m/%d/%Y')
    
    # Map hourly columns
    # Source columns: 1:00 ... 11:00, 12:00, 13:00 ... 23:00, 24:00:00
    # Target columns: 1:00 AM ... 11:00 AM, 12:00 AM, 1:00 PM ... 11:00 PM, 12:00 PM
    
    for h in range(1, 25):
        if h == 24:
            src_col = '24:00:00'
            tgt_col = '12:00 PM'
        else:
            src_col = f'{h}:00'
            if h == 12:
                tgt_col = '12:00 AM'
            elif h < 12:
                tgt_col = f'{h}:00 AM'
            else:
                tgt_col = f'{h-12}:00 PM'
        
        out[tgt_col] = source[src_col]
        
    return out.reset_index(drop=True)
