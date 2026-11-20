import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying the source
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format is observed as 'm/d/Y' or 'mm/dd/yyyy', pd.to_datetime handles this flexibly
    # Target format is 'mm/dd/yyyy'
    df['date'] = pd.to_datetime(df['Date']).dt.strftime('%m/%d/%Y')
    
    # 2. Rename hourly columns
    rename_map = {}
    for i in range(1, 25):
        rename_map[f'Hr {i}'] = f'Hour {i}'
    
    df = df.rename(columns=rename_map)
    
    # 3. Select target columns in the correct order
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    result = df[target_columns]
    
    return result.reset_index(drop=True)
