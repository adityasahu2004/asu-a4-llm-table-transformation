import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column. Format is "%a %m/%d/%Y" based on sample "Thu 10/01/2009"
    dates = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    out = pd.DataFrame(index=source.index)
    
    # Create 'date' column formatted as MM/DD/YYYY
    out['date'] = dates.dt.strftime('%m/%d/%Y')
    
    # Map the 24 hourly columns
    for h in range(1, 25):
        if h < 24:
            src_col = f'{h}:00'
        else:
            # The 24th hour column is named "24:00:00" in the source
            src_col = '24:00:00'
        
        target_col = f'Hour {h}'
        out[target_col] = source[src_col]
        
    return out.reset_index(drop=True)
