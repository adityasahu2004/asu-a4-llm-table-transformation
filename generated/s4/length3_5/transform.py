import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the source date string 'M/D/YYYY' to datetime
    dt_series = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format to target string 'YYYY-MM-DD HH:MM:SS'
    # The target sample shows "2011-01-01 00:00:00"
    out = pd.DataFrame()
    out['date'] = dt_series.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Rename value columns to Hour columns
    for i in range(1, 25):
        out[f'Hour {i}'] = source[f'value{i}']
        
    return out.reset_index(drop=True)
