import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format date as YYYY-MM-DD 00:00:00
    formatted_date = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Define the target column names for hours 1-24
    target_hour_cols = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    # Map source hourly columns to target columns
    # Source columns are 'Hour 1', 'Hour 2', ... 'Hour 24'
    out = pd.DataFrame()
    out['date'] = formatted_date
    
    for i, col_name in enumerate(target_hour_cols, start=1):
        src_col = f'Hour {i}'
        out[col_name] = source[src_col]
        
    return out
