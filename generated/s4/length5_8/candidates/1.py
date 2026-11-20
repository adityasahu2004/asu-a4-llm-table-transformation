import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse and format the date column
    # Source format is inferred as '%m/%d/%Y' based on samples like "7/3/2015"
    # Target format is 'yyyy-mm-dd 00:00:00'
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    formatted_date = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # 2. Create the output DataFrame
    out = pd.DataFrame()
    out['date'] = formatted_date
    
    # 3. Rename and project hourly columns
    # Source: 'Hour 1' ... 'Hour 24'
    # Target: 'value1' ... 'value24'
    for i in range(1, 25):
        out[f'value{i}'] = source[f'Hour {i}']
        
    # 4. Reset index to match standard output expectations
    return out.reset_index(drop=True)
