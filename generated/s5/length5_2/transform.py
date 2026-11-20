import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse CST to datetime to extract date
    # Format is "DayOfWeek MM/DD/YYYY" e.g., "Sat 12/01/2012"
    dt = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    out = pd.DataFrame(index=source.index)
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Map hour columns 1:00 through 24:00:00 to value1 through value24
    # Note: 24:00:00 is the 24th hour
    for h in range(1, 25):
        if h < 24:
            src_col = f'{h}:00'
        else:
            src_col = '24:00:00'
        out[f'value{h}'] = source[src_col]
        
    return out.reset_index(drop=True)
