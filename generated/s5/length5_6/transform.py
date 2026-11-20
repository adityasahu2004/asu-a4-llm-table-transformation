import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse and format the date column
    # Source format: MM/DD/YYYY
    # Target format: YYYY-MM-DD 00:00:00
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    formatted_dates = dates.dt.strftime('%Y-%m-%d 00:00:00')
    
    # 2. Define the mapping from source AM/PM columns to target value1...value24
    # Order: 1AM, 2AM, ..., 11AM, 12PM, 1PM, ..., 11PM, 12AM
    hour_labels = []
    # 1 AM to 11 AM
    for h in range(1, 12):
        hour_labels.append(f'{h}:00 AM')
    # 12 PM (Noon)
    hour_labels.append('12:00 PM')
    # 1 PM to 11 PM
    for h in range(1, 12):
        hour_labels.append(f'{h}:00 PM')
    # 12 AM (Midnight)
    hour_labels.append('12:00 AM')
    
    # 3. Build the new dataframe
    out = pd.DataFrame()
    out['date'] = formatted_dates
    
    # Map source columns to value1...value24
    for i, src_col in enumerate(hour_labels, start=1):
        out[f'value{i}'] = source[src_col]
        
    # 4. Reset index to ensure clean integer index
    return out.reset_index(drop=True)
