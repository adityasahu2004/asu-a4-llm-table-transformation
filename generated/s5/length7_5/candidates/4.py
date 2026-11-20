import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame()
    
    # Extract month name
    out['month'] = dates.dt.strftime('%B')
    
    # Extract daytype: weekday (Mon-Fri) or weekend (Sat-Sun)
    # dayofweek: Monday=0, ..., Sunday=6
    out['daytype'] = dates.dt.dayofweek.apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # Define the mapping from source hour columns to target hr columns
    # Source columns in order:
    src_hour_cols = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM',
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM',
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM',
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    # Map to hr1 ... hr24
    for i, col in enumerate(src_hour_cols):
        out[f'hr{i+1}'] = source[col]
        
    return out.reset_index(drop=True)
