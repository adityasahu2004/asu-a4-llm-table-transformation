import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Define the mapping from source AM/PM columns to chronological order (value1 to value24)
    # 12:00 AM is 00:00 (Hour 1)
    # 1:00 AM is 01:00 (Hour 2)
    # ...
    # 11:00 AM is 11:00 (Hour 12)
    # 12:00 PM is 12:00 (Hour 13)
    # 1:00 PM is 13:00 (Hour 14)
    # ...
    # 11:00 PM is 23:00 (Hour 24)
    
    col_map = {
        '12:00 AM': 'value1',
        '1:00 AM': 'value2',
        '2:00 AM': 'value3',
        '3:00 AM': 'value4',
        '4:00 AM': 'value5',
        '5:00 AM': 'value6',
        '6:00 AM': 'value7',
        '7:00 AM': 'value8',
        '8:00 AM': 'value9',
        '9:00 AM': 'value10',
        '10:00 AM': 'value11',
        '11:00 AM': 'value12',
        '12:00 PM': 'value13',
        '1:00 PM': 'value14',
        '2:00 PM': 'value15',
        '3:00 PM': 'value16',
        '4:00 PM': 'value17',
        '5:00 PM': 'value18',
        '6:00 PM': 'value19',
        '7:00 PM': 'value20',
        '8:00 PM': 'value21',
        '9:00 PM': 'value22',
        '10:00 PM': 'value23',
        '11:00 PM': 'value24'
    }

    # Create a new dataframe with the mapped columns
    out = source[list(col_map.keys())].copy()
    out = out.rename(columns=col_map)
    
    # Ensure the order is value1 to value24
    out = out[['value' + str(i) for i in range(1, 25)]]
    
    # Format the date column
    # Source date is MM/DD/YYYY
    # Target date is YYYY-MM-DD 00:00:00
    out['date'] = pd.to_datetime(source['date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d 00:00:00')
    
    # Reorder columns to match target: date, value1, ..., value24
    result = pd.concat([out['date'], out[['value' + str(i) for i in range(1, 25)]]], axis=1)
    
    return result
