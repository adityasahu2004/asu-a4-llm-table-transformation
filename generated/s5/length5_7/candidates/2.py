import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse and format the date column
    # Source format is M/D/YYYY or MM/DD/YYYY
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # 2. Rename hourly columns from "1"..."24" to "value1"..."value24"
    for h in range(1, 25):
        out[f'value{h}'] = source[str(h)]
        
    return out
