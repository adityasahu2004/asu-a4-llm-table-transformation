import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the CST column to datetime
    dt = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    # Create the Date column in MM/DD/YYYY format
    out = pd.DataFrame()
    out['Date'] = dt.strftime('%m/%d/%Y')
    
    # Map source hour columns to target hour columns
    # Source: '1:00'...'23:00', '24:00:00'
    # Target: 'Hr 1'...'Hr 24'
    
    for h in range(1, 24):
        out[f'Hr {h}'] = source[f'{h}:00']
    
    # Handle the 24th hour specifically as its source name is '24:00:00'
    out['Hr 24'] = source['24:00:00']
    
    return out
