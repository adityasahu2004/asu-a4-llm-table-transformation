import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the CST column to datetime
    # Format is "DayOfWeek MM/DD/YYYY", e.g., "Sat 12/01/2012"
    dt = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    # Create the target DataFrame
    out = pd.DataFrame()
    out['Date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Map source hourly columns to target names
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hr 1', 'Hr 2', ..., 'Hr 23', 'Hr 24'
    
    for h in range(1, 24):
        src_col = f'{h}:00'
        tgt_col = f'Hr {h}'
        out[tgt_col] = source[src_col].values
        
    # Handle the 24th hour specifically due to different source format
    out['Hr 24'] = source['24:00:00'].values
    
    return out
