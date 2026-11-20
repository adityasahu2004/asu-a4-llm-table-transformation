import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format date to ISO 8601 with 00:00:00
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Define the mapping from source value columns to target hour labels
    # Standard assumption: value1=1AM, value12=12PM, value24=12AM
    col_map = {
        'value1': '1:00 AM',
        'value2': '2:00 AM',
        'value3': '3:00 AM',
        'value4': '4:00 AM',
        'value5': '5:00 AM',
        'value6': '6:00 AM',
        'value7': '7:00 AM',
        'value8': '8:00 AM',
        'value9': '9:00 AM',
        'value10': '10:00 AM',
        'value11': '11:00 AM',
        'value12': '12:00 PM', # Noon
        'value13': '1:00 PM',
        'value14': '2:00 PM',
        'value15': '3:00 PM',
        'value16': '4:00 PM',
        'value17': '5:00 PM',
        'value18': '6:00 PM',
        'value19': '7:00 PM',
        'value20': '8:00 PM',
        'value21': '9:00 PM',
        'value22': '10:00 PM',
        'value23': '11:00 PM',
        'value24': '12:00 AM' # Midnight
    }
    
    # Rename columns
    out = out.join(source.rename(columns=col_map))
    
    # Select and order columns exactly as per target schema
    target_cols = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', 
        '12:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', 
        '12:00 PM'
    ]
    
    return out[target_cols]
