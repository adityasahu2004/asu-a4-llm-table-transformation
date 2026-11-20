import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    # The source format is M/D/YYYY or MM/DD/YYYY
    parsed_dates = pd.to_datetime(source['Date'], format='mixed', dayfirst=False)
    
    # 2. Format the date to the target string format: YYYY-MM-DD 00:00:00
    formatted_dates = parsed_dates.dt.strftime('%Y-%m-%d 00:00:00')
    
    # 3. Create the output dataframe
    # We start with the formatted dates
    out = pd.DataFrame({'date': formatted_dates})
    
    # 4. Rename and add the hourly value columns
    # Source columns are strings '1' through '24'
    # Target columns are 'value1' through 'value24'
    for h in range(1, 25):
        out[f'value{h}'] = source[str(h)]
        
    return out
