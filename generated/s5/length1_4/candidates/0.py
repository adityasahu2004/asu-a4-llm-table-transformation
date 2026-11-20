import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date string
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create the cst column with format "DayOfWeek MM/DD/YYYY"
    cst = dt.dt.strftime('%a %m/%d/%Y')
    
    # Rename hour columns from "1"..."24" to "1:00"..."24:00"
    # The source columns are strings '1', '2', ..., '24'
    rename_map = {str(h): f"{h}:00" for h in range(1, 25)}
    
    # Select and rename
    result = pd.DataFrame()
    result['cst'] = cst
    for h in range(1, 25):
        result[f"{h}:00"] = source[str(h)]
        
    return result.reset_index(drop=True)
