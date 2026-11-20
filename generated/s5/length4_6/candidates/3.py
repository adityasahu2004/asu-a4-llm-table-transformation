import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date and format it as requested
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    date_formatted = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Define the mapping from Source Hour columns to Target Hour columns
    # Based on the target column order provided in the schema
    hour_mapping = {
        'Hr 1': '1:00 AM',
        'Hr 2': '2:00 AM',
        'Hr 3': '3:00 AM',
        'Hr 4': '4:00 AM',
        'Hr 5': '5:00 AM',
        'Hr 6': '6:00 AM',
        'Hr 7': '7:00 AM',
        'Hr 8': '8:00 AM',
        'Hr 9': '9:00 AM',
        'Hr 10': '10:00 AM',
        'Hr 11': '11:00 AM',
        'Hr 12': '12:00 AM',
        'Hr 13': '1:00 PM',
        'Hr 14': '2:00 PM',
        'Hr 15': '3:00 PM',
        'Hr 16': '4:00 PM',
        'Hr 17': '5:00 PM',
        'Hr 18': '6:00 PM',
        'Hr 19': '7:00 PM',
        'Hr 20': '8:00 PM',
        'Hr 21': '9:00 PM',
        'Hr 22': '10:00 PM',
        'Hr 23': '11:00 PM',
        'Hr 24': '12:00 PM'
    }
    
    # Select and rename the hour columns
    out = source[list(hour_mapping.keys())].copy()
    out = out.rename(columns=hour_mapping)
    
    # Add the formatted date column
    out.insert(0, 'date', date_formatted)
    
    # Ensure the column order matches the target specification
    target_cols = ['date'] + list(hour_mapping.values())
    out = out[target_cols]
    
    return out
