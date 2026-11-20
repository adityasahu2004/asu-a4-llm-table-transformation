import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    parsed_dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format to target string format
    formatted_dates = parsed_dates.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Create the result DataFrame
    result = pd.DataFrame()
    result['Date'] = formatted_dates
    
    # Map value columns to Hr columns
    for i in range(1, 25):
        result[f'Hr {i}'] = source[f'value{i}']
        
    return result.reset_index(drop=True)
