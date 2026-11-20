import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the CST column to datetime
    # Format: "Sat 12/01/2012" -> %a %m/%d/%Y
    dt = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    # Create the 'date' column formatted as MM/DD/YYYY
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Map source hour columns to target hour columns
    # Source: "1:00" ... "23:00", "24:00:00"
    # Target: "Hour 1" ... "Hour 24"
    
    for h in range(1, 24):
        src_col = f"{h}:00"
        tgt_col = f"Hour {h}"
        out[tgt_col] = source[src_col]
        
    # Handle the 24th hour specifically due to different source format "24:00:00"
    out['Hour 24'] = source['24:00:00']
    
    return out
