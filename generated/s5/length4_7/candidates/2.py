import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format as MM/DD/YYYY
    dt = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Mapping from source hour index (1-24) to target column name
    # Source cols: '1:00', '2:00', ..., '11:00', '12:00', '13:00', ..., '23:00', '24:00:00'
    # Target cols: '1:00 AM', ..., '11:00 AM', '12:00 AM', '1:00 PM', ..., '11:00 PM', '12:00 PM'
    
    hour_mapping = {
        '1:00': '1:00 AM',
        '2:00': '2:00 AM',
        '3:00': '3:00 AM',
        '4:00': '4:00 AM',
        '5:00': '5:00 AM',
        '6:00': '6:00 AM',
        '7:00': '7:00 AM',
        '8:00': '8:00 AM',
        '9:00': '9:00 AM',
        '10:00': '10:00 AM',
        '11:00': '11:00 AM',
        '12:00': '12:00 AM',
        '13:00': '1:00 PM',
        '14:00': '2:00 PM',
        '15:00': '3:00 PM',
        '16:00': '4:00 PM',
        '17:00': '5:00 PM',
        '18:00': '6:00 PM',
        '19:00': '7:00 PM',
        '20:00': '8:00 PM',
        '21:00': '9:00 PM',
        '22:00': '10:00 PM',
        '23:00': '11:00 PM',
        '24:00:00': '12:00 PM'
    }
    
    # Reorder and rename columns
    # The target schema lists the hours in a specific order: 
    # 1AM..11AM, 12AM, 1PM..11PM, 12PM
    # We construct the dataframe in this specific column order.
    
    ordered_target_cols = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', 
        '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', 
        '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    # Map back to source names to extract data
    source_cols_for_order = [
        '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', 
        '9:00', '10:00', '11:00', '12:00', 
        '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', 
        '21:00', '22:00', '23:00', '24:00:00'
    ]
    
    for target_name, source_name in zip(ordered_target_cols, source_cols_for_order):
        out[target_name] = source[source_name]
        
    return out
