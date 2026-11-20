import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target format.
    
    1. Parses the 'date' column.
    2. Sorts by date.
    3. Formats the date into 'cst' (DayOfWeek MM/DD/YYYY).
    4. Renames 'value1'...'value24' to '1:00'...'24:00'.
    5. Selects the relevant columns.
    """
    # Make a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the date column
    df['date_parsed'] = pd.to_datetime(df['date'])
    
    # Sort by date to ensure chronological order as seen in target
    df = df.sort_values('date_parsed').reset_index(drop=True)
    
    # Format the date into the 'cst' column format: "DayOfWeek MM/DD/YYYY"
    # %a gives abbreviated weekday name (e.g., Sat, Sun)
    df['cst'] = df['date_parsed'].dt.strftime('%a %m/%d/%Y')
    
    # Define the mapping for value columns to time columns
    # Source: value1, value2, ..., value24
    # Target: 1:00, 2:00, ..., 24:00
    rename_map = {}
    for i in range(1, 25):
        rename_map[f'value{i}'] = f'{i}:00'
        
    # Rename the columns
    df = df.rename(columns=rename_map)
    
    # Select the final columns in the correct order
    # Target columns: cst, 1:00, 2:00, ..., 24:00
    final_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # Select only the required columns
    result = df[final_columns]
    
    # Ensure numeric types for the value columns (they should already be float64)
    for col in result.columns[1:]:
        result[col] = pd.to_numeric(result[col], errors='coerce')
        
    return result
