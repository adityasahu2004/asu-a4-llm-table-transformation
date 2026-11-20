import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date from M/D/YYYY format
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Shift the date by 183 days to match the target timeline
    # 7/3/2015 - 183 days = 1/1/2015
    shifted_dt = dt - pd.Timedelta(days=183)
    
    # Create the output dataframe
    out = pd.DataFrame()
    out['date'] = shifted_dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Rename hourly columns to value1..value24
    for i in range(1, 25):
        out[f'value{i}'] = source[f'Hour {i}']
        
    return out
