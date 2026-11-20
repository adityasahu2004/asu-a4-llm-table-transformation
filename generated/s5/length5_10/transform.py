import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date from source
    # Format is "DayOfWeek MM/DD/YYYY", e.g., "Thu 10/01/2009"
    parsed_dates = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # Create the output dataframe with the formatted date string
    out = pd.DataFrame()
    out['date'] = parsed_dates.dt.strftime('%a %m/%d/%Y')
    
    # Map the 24 hourly columns to value1...value24
    for h in range(1, 25):
        # Determine source column name
        if h < 24:
            src_col = f"{h}:00"
        else:
            src_col = "24:00:00"
        
        # Assign to target column
        out[f"value{h}"] = source[src_col]
        
    return out.reset_index(drop=True)
