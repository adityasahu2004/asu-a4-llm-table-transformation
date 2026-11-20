import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column and format it as MM/DD/YYYY
    parsed_dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    formatted_dates = parsed_dates.dt.strftime('%m/%d/%Y')
    
    # Initialize the result DataFrame
    result = pd.DataFrame()
    result['date'] = formatted_dates
    
    # Rename hourly columns from 'Hr X' to 'Hour X'
    for h in range(1, 25):
        result[f'Hour {h}'] = source[f'Hr {h}']
        
    return result.reset_index(drop=True)
