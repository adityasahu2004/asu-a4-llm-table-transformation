import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the Date column to datetime for sorting
    # Format is e.g., "Thu 10/01/2009"
    df['_parsed_date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    
    # Sort by the parsed date
    df = df.sort_values('_parsed_date').reset_index(drop=True)
    
    # Rename the Date column to the correct format string if needed, 
    # but first ensure it matches the target format exactly.
    # The target format is "%a %m/%d/%Y" (e.g., "Wed 01/01/2003")
    df['Date'] = df['_parsed_date'].dt.strftime('%a %m/%d/%Y')
    
    # Define the mapping for hourly columns
    # Source: "1:00", "2:00", ..., "23:00", "24:00:00"
    # Target: "Hr 1", "Hr 2", ..., "Hr 23", "Hr 24"
    
    # Map hours 1-23
    for h in range(1, 24):
        src_col = f"{h}:00"
        tgt_col = f"Hr {h}"
        df[tgt_col] = df[src_col]
        
    # Map hour 24 specifically due to different source format "24:00:00"
    df['Hr 24'] = df['24:00:00']
    
    # Select only the required columns in the correct order
    cols = ['Date'] + [f'Hr {h}' for h in range(1, 25)]
    result = df[cols]
    
    # Ensure dtypes are correct (float64 for hours, str for Date)
    # Date is already str from strftime
    for h in range(1, 25):
        result[f'Hr {h}'] = result[f'Hr {h}'].astype('float64')
        
    return result.reset_index(drop=True)
