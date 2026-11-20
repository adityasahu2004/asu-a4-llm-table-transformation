import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source dataframe by:
    1. Parsing the 'Date' column.
    2. Formatting the date into the 'cst' column with format 'Day MM/DD/YYYY'.
    3. Renaming numeric columns 1-24 to '1:00'-'24:00'.
    4. Dropping the 'Class' column.
    """
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the Date column
    # The source format is MM/DD/YYYY (e.g., "7/3/2013")
    df['Date_parsed'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # Create the 'cst' column with format "Day MM/DD/YYYY"
    # Example: "Tue 01/01/2013"
    # %a gives abbreviated weekday name (Tue, Wed, etc.)
    # %m/%d/%Y gives MM/DD/YYYY
    df['cst'] = df['Date_parsed'].dt.strftime('%a %m/%d/%Y')
    
    # Rename the numeric columns from '1'...'24' to '1:00'...'24:00'
    # Identify numeric columns (those with integer names 1-24)
    numeric_cols = [str(i) for i in range(1, 25)]
    new_names = {str(i): f"{i}:00" for i in range(1, 25)}
    
    df = df.rename(columns=new_names)
    
    # Select the required columns: 'cst' and the renamed numeric columns
    # Ensure 'cst' is first
    cols_to_keep = ['cst'] + [f"{i}:00" for i in range(1, 25)]
    
    # Filter to ensure only these columns exist
    df = df[cols_to_keep]
    
    # Sort by the parsed date to ensure chronological order if needed
    # We can sort by the 'cst' string if we assume the format sorts correctly, 
    # but it's safer to use the parsed date if we kept it. 
    # Since we didn't keep 'Date_parsed' in the final select, let's re-parse or sort by index if stable.
    # However, strftime output "Tue 01/01/2013" does not sort correctly lexicographically.
    # Let's add the parsed date back temporarily for sorting, then drop.
    
    # Actually, we can just sort by the original 'Date' column if we hadn't dropped it, 
    # or parse 'cst' back. Easier: parse 'Date' again for sorting.
    # But wait, we can just sort by the index if the input was ordered, or re-parse.
    
    # Let's parse 'cst' back to datetime for sorting? 
    # Format: "%a %m/%d/%Y"
    # It's robust enough.
    df['Date_sort'] = pd.to_datetime(df['cst'], format='%a %m/%d/%Y')
    df = df.sort_values(by='Date_sort')
    df = df.drop(columns=['Date_sort'])
    
    # Reset index
    df = df.reset_index(drop=True)
    
    return df
