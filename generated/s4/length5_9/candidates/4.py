import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create the output dataframe with the formatted date
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Map source hourly columns to target value columns
    for h in range(1, 25):
        out[f'value{h}'] = source[f'Hr {h}']
        
    return out
