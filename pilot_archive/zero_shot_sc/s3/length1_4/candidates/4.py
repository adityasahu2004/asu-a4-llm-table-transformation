import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame by:
    1. Parsing the 'Date' column.
    2. Creating a 'cst' column with formatted dates.
    3. Renaming columns 1-24 to 1:00-24:00.
    4. Dropping the 'Class' column.
    5. Sorting by date.
    """
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Parse dates
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Format date to 'cst' column
    df['cst'] = df['Date'].dt.strftime('%a %m/%d/%Y')
    
    # Define new column names for hours
    hour_cols = {str(i): f"{i}:00" for i in range(1, 25)}
    
    # Rename columns
    df.rename(columns=hour_cols, inplace=True)
    
    # Select and order columns: 'cst' followed by the hour columns
    # Identify hour columns dynamically based on the new names
    hour_col_names = [f"{i}:00" for i in range(1, 25)]
    
    # Select columns
    result = df[['cst'] + hour_col_names]
    
    # Sort by the original date to ensure correct chronological order
    # We need to keep the date for sorting, then drop it
    result = result.set_index('cst').sort_index(kind='mergesort').reset_index()
    
    # Actually, sorting by string 'cst' might not be perfect if we just reset index.
    # Better to sort by the datetime 'Date' before dropping it.
    
    # Let's refine the selection and sorting
    df_sorted = df.sort_values('Date')
    result = df_sorted[['cst'] + hour_col_names]
    
    return result
