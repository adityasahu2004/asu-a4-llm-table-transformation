import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    dates = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame()
    out['date'] = dates.dt.strftime('%m/%d/%Y')
    
    # Map source hourly columns to target hourly columns
    # Source columns: "1:00" ... "23:00", "24:00:00"
    # Target columns: "Hour 1" ... "Hour 24"
    
    for h in range(1, 25):
        if h == 24:
            src_col = '24:00:00'
        else:
            src_col = f'{h}:00'
        
        out[f'Hour {h}'] = source[src_col]
        
    return out
