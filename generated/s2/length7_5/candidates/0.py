import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Derive month name
    month = dt.dt.strftime('%B')
    
    # Derive daytype: 5=Sat, 6=Sun are weekends
    daytype = dt.dt.dayofweek.apply(lambda d: 'weekend' if d >= 5 else 'weekday')
    
    # Map source columns to target hr1-hr24
    # Source order in schema: 1AM, 2AM, ..., 11AM, 12AM, 1PM, ..., 11PM, 12PM
    # Chronological order:
    # 1: 12:00 AM
    # 2: 1:00 AM
    # 3: 2:00 AM
    # ...
    # 11: 10:00 AM
    # 12: 11:00 AM
    # 13: 12:00 PM
    # 14: 1:00 PM
    # ...
    # 24: 11:00 PM
    
    col_map = {
        'hr1': '12:00 AM',
        'hr2': '1:00 AM',
        'hr3': '2:00 AM',
        'hr4': '3:00 AM',
        'hr5': '4:00 AM',
        'hr6': '5:00 AM',
        'hr7': '6:00 AM',
        'hr8': '7:00 AM',
        'hr9': '8:00 AM',
        'hr10': '9:00 AM',
        'hr11': '10:00 AM',
        'hr12': '11:00 AM',
        'hr13': '12:00 PM',
        'hr14': '1:00 PM',
        'hr15': '2:00 PM',
        'hr16': '3:00 PM',
        'hr17': '4:00 PM',
        'hr18': '5:00 PM',
        'hr19': '6:00 PM',
        'hr20': '7:00 PM',
        'hr21': '8:00 PM',
        'hr22': '9:00 PM',
        'hr23': '10:00 PM',
        'hr24': '11:00 PM'
    }
    
    out = pd.DataFrame()
    out['month'] = month
    out['daytype'] = daytype
    
    for target_col, source_col in col_map.items():
        out[target_col] = source[source_col]
        
    return out.reset_index(drop=True)
