import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Format date to MM/DD/YYYY
    out = pd.DataFrame()
    out['date'] = dates.dt.strftime('%m/%d/%Y')
    
    # Define the mapping from source integer columns to target string columns
    # Source columns are strings "1" through "24"
    target_names = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM',
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    for i, target_name in enumerate(target_names):
        source_col = str(i + 1)
        out[target_name] = source[source_col]
        
    return out
