import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format to YYYY-MM-DD 00:00:00
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    out_date = dates.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Define the mapping from source column names to target column names
    rename_map = {
        'Hour 1': '1:00 AM',
        'Hour 2': '2:00 AM',
        'Hour 3': '3:00 AM',
        'Hour 4': '4:00 AM',
        'Hour 5': '5:00 AM',
        'Hour 6': '6:00 AM',
        'Hour 7': '7:00 AM',
        'Hour 8': '8:00 AM',
        'Hour 9': '9:00 AM',
        'Hour 10': '10:00 AM',
        'Hour 11': '11:00 AM',
        'Hour 12': '12:00 AM',
        'Hour 13': '1:00 PM',
        'Hour 14': '2:00 PM',
        'Hour 15': '3:00 PM',
        'Hour 16': '4:00 PM',
        'Hour 17': '5:00 PM',
        'Hour 18': '6:00 PM',
        'Hour 19': '7:00 PM',
        'Hour 20': '8:00 PM',
        'Hour 21': '9:00 PM',
        'Hour 22': '10:00 PM',
        'Hour 23': '11:00 PM',
        'Hour 24': '12:00 PM'
    }
    
    # Select and rename the hourly columns
    hourly_cols = [f'Hour {i}' for i in range(1, 25)]
    target_cols = [rename_map[col] for col in hourly_cols]
    
    # Create the result dataframe
    result = pd.DataFrame(index=source.index)
    result['date'] = out_date
    
    for src_col, tgt_col in zip(hourly_cols, target_cols):
        result[tgt_col] = source[src_col]
        
    return result.reset_index(drop=True)
