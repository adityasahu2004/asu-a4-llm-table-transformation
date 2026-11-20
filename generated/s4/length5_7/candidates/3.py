import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date string to datetime
    dates = pd.to_datetime(source['Date'])
    
    # Format to YYYY-MM-DD HH:MM:SS
    formatted_dates = dates.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Create the result dataframe starting with the date column
    result = pd.DataFrame({'date': formatted_dates}, index=source.index)
    
    # Rename and add the 24 hourly value columns
    for h in range(1, 25):
        result[f'value{h}'] = source[h]
        
    return result.reset_index(drop=True)
