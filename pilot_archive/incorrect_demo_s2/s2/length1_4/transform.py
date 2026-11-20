import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create the target 'cst' column with format "DayOfWeek MM/DD/YYYY"
    # %a gives abbreviated weekday name (e.g., Tue)
    cst_formatted = dt.dt.strftime('%a %m/%d/%Y')
    
    # Build the result dataframe
    result = pd.DataFrame()
    result['cst'] = cst_formatted
    
    # Map source columns 1-24 to target columns 1:00-24:00
    for h in range(1, 25):
        result[f'{h}:00'] = source[str(h)]
        
    return result
