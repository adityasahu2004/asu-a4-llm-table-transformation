import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Format Date
    # Source is like "7/3/2015", Target is "2015-01-01 00:00:00"
    parsed_dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    out = pd.DataFrame()
    out['date'] = parsed_dates.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Rename Columns
    # Mapping from Source "Hour N" to Target "H:MM AM/PM"
    # Note the specific AM/PM labels in the target schema:
    # Hour 12 maps to "12:00 AM" in the target column list provided.
    # Hour 24 maps to "12:00 PM" in the target column list provided.
    
    rename_map = {}
    for h in range(1, 25):
        src_col = f'Hour {h}'
        if h == 12:
            tgt_col = '12:00 AM'
        elif h == 24:
            tgt_col = '12:00 PM'
        else:
            period = 'AM' if h < 12 else 'PM'
            display_h = h if h < 13 else h - 12
            tgt_col = f'{display_h}:00 {period}'
        rename_map[src_col] = tgt_col
        
    # Apply renaming to the subset of hourly columns
    hourly_data = source[[f'Hour {h}' for h in range(1, 25)]].rename(columns=rename_map)
    
    # Concatenate date and hourly data
    out = pd.concat([out, hourly_data], axis=1)
    
    # Ensure column order matches target schema exactly
    target_cols = ['date']
    target_cols += ['1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM',
                    '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM']
    
    return out[target_cols].reset_index(drop=True)
