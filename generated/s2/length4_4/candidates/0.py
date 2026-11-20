import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Format the date as MM/DD/YYYY
    out = pd.DataFrame()
    out['date'] = dates.dt.strftime('%m/%d/%Y')
    
    # Define the target column names in order
    target_cols = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM',
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM',
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM',
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    # Map source columns 1-24 to the target names
    for i, col_name in enumerate(target_cols):
        src_col = str(i + 1)
        out[col_name] = source[src_col]
        
    return out
