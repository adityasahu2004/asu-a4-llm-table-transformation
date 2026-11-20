import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create the output DataFrame
    out = pd.DataFrame(index=source.index)
    
    # Format date as MM/DD/YYYY
    out['Date'] = dates.dt.strftime('%m/%d/%Y')
    
    # Rename hourly columns from "1"..."24" to "Hr 1"..."Hr 24"
    for h in range(1, 25):
        out[f'Hr {h}'] = source[str(h)]
        
    return out.reset_index(drop=True)
