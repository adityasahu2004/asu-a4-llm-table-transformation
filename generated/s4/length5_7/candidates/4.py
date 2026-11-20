import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create the output dataframe
    out = pd.DataFrame()
    
    # Format date as required: YYYY-MM-DD 00:00:00
    out['date'] = dates.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Rename hourly columns from "1"..."24" to "value1"..."value24"
    for h in range(1, 25):
        out[f'value{h}'] = source[str(h)]
        
    # Reset index to ensure clean output
    return out.reset_index(drop=True)
