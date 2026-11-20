import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format as MM/DD/YYYY
    parsed_dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    date_str = parsed_dates.dt.strftime('%m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame()
    out['date'] = date_str
    
    # Rename hourly columns from 'Hr X' to 'Hour X'
    for i in range(1, 25):
        out[f'Hour {i}'] = source[f'Hr {i}']
        
    return out.reset_index(drop=True)
