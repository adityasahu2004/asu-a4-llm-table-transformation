import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Filter for RESIDENT class
    df = source[source['Class'] == 'RESIDENT'].copy()
    
    # Parse and format the date
    # Source format is variable m/d/Y, e.g., "7/3/2013"
    df['date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d 00:00:00')
    
    # Define the mapping for hour columns
    # Source columns are strings "1" to "24"
    # Target columns are "value1" to "value24"
    rename_map = {str(h): f'value{h}' for h in range(1, 25)}
    
    # Rename the value columns
    df = df.rename(columns=rename_map)
    
    # Select and order columns
    target_cols = ['date'] + [f'value{h}' for h in range(1, 25)]
    
    result = df[target_cols]
    
    return result.reset_index(drop=True)
