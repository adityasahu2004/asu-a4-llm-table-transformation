import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format date to YYYY-MM-DD 00:00:00
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Map source columns to Hour 1-24
    # Hour 1: 12:00 AM
    # Hour 2: 1:00 AM
    # ...
    # Hour 12: 11:00 AM
    # Hour 13: 12:00 PM
    # Hour 14: 1:00 PM
    # ...
    # Hour 24: 11:00 PM
    
    mapping = {
        'Hour 1': '12:00 AM',
        'Hour 2': '1:00 AM',
        'Hour 3': '2:00 AM',
        'Hour 4': '3:00 AM',
        'Hour 5': '4:00 AM',
        'Hour 6': '5:00 AM',
        'Hour 7': '6:00 AM',
        'Hour 8': '7:00 AM',
        'Hour 9': '8:00 AM',
        'Hour 10': '9:00 AM',
        'Hour 11': '10:00 AM',
        'Hour 12': '11:00 AM',
        'Hour 13': '12:00 PM',
        'Hour 14': '1:00 PM',
        'Hour 15': '2:00 PM',
        'Hour 16': '3:00 PM',
        'Hour 17': '4:00 PM',
        'Hour 18': '5:00 PM',
        'Hour 19': '6:00 PM',
        'Hour 20': '7:00 PM',
        'Hour 21': '8:00 PM',
        'Hour 22': '9:00 PM',
        'Hour 23': '10:00 PM',
        'Hour 24': '11:00 PM'
    }
    
    for target_col, source_col in mapping.items():
        out[target_col] = source[source_col]
        
    return out.reset_index(drop=True)
