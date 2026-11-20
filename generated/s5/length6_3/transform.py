import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create the output dataframe
    out = pd.DataFrame()
    
    # Format the date as requested: YYYY-MM-DD 00:00:00
    out['Date'] = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Rename and select the hourly value columns
    for i in range(1, 25):
        out[f'Hr {i}'] = source[f'value{i}']
        
    # Reset index to ensure clean integer index
    return out.reset_index(drop=True)
