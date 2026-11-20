import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date
    dt_series = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format date as required
    out = pd.DataFrame()
    out['date'] = dt_series.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Mapping from chronological hour index (1-24) to source column names
    # Source order: 1-11 AM, 12 AM, 1-11 PM, 12 PM
    # Chronological: 1=1AM, 2=2AM, ..., 11=11AM, 12=12AM, 13=1PM, ..., 23=11PM, 24=12PM
    
    hour_mapping = {
        1: '1:00 AM',
        2: '2:00 AM',
        3: '3:00 AM',
        4: '4:00 AM',
        5: '5:00 AM',
        6: '6:00 AM',
        7: '7:00 AM',
        8: '8:00 AM',
        9: '9:00 AM',
        10: '10:00 AM',
        11: '11:00 AM',
        12: '12:00 AM',
        13: '1:00 PM',
        14: '2:00 PM',
        15: '3:00 PM',
        16: '4:00 PM',
        17: '5:00 PM',
        18: '6:00 PM',
        19: '7:00 PM',
        20: '8:00 PM',
        21: '9:00 PM',
        22: '10:00 PM',
        23: '11:00 PM',
        24: '12:00 PM'
    }
    
    for h in range(1, 25):
        out[f'Hour {h}'] = source[hour_mapping[h]]
        
    return out
