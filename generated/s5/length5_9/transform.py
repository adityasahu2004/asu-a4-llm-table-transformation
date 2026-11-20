import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format to ISO-like string with time
    dt_series = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    out = pd.DataFrame()
    out['date'] = dt_series.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Rename hourly columns Hr 1..24 to value1..value24
    for i in range(1, 25):
        out[f'value{i}'] = source[f'Hr {i}']
        
    return out.reset_index(drop=True)
