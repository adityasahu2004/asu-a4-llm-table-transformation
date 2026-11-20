import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates and shift by 182 days
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    shifted_dates = dates - pd.Timedelta(days=182)
    
    # Construct output dataframe
    out = pd.DataFrame(index=source.index)
    out['Date'] = shifted_dates.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Rename Hour columns to Hr columns
    for h in range(1, 25):
        out[f'Hr {h}'] = source[f'Hour {h}']
        
    return out.reset_index(drop=True)
