import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column to ensure correct formatting
    # The source format is %m/%d/%Y (e.g., "7/3/2013")
    # The target format is %a %m/%d/%Y (e.g., "Tue 01/01/2013")
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create the new dataframe with the formatted date column
    out = pd.DataFrame()
    out['cst'] = dates.dt.strftime('%a %m/%d/%Y')
    
    # Rename the hourly columns from "1", "2", ... "24" to "1:00", "2:00", ... "24:00"
    for h in range(1, 25):
        out[f'{h}:00'] = source[str(h)]
        
    return out.reset_index(drop=True)
