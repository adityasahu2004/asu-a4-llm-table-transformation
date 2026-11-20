import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the source date column to datetime
    # Source format is "E m/d/yyyy" (e.g., "Thu 10/01/2009")
    dt = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Create the target date string: "E mm/dd/yyyy" (e.g., "Wed 01/01/2003")
    out_date = dt.dt.strftime('%a %m/%d/%Y')
    
    # Initialize the output dataframe with the date column
    result = pd.DataFrame({'Date': out_date}, index=source.index)
    
    # Map source hourly columns to target hourly columns
    # Source: "1:00", "2:00", ..., "23:00", "24:00:00"
    # Target: "Hr 1", "Hr 2", ..., "Hr 23", "Hr 24"
    for h in range(1, 24):
        result[f'Hr {h}'] = source[f'{h}:00']
    
    # Handle the 24th hour specifically due to different suffix in source
    result['Hr 24'] = source['24:00:00']
    
    return result.reset_index(drop=True)
