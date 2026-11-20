import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from a wide format with 'value1'-'value24' columns
    to a target format with '1:00'-'24:00' columns and a formatted date column 'cst'.
    """
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the date column. The format in source is 'M/D/YYYY' or 'MM/DD/YYYY'.
    # We use pd.to_datetime which automatically infers this format.
    df['parsed_date'] = pd.to_datetime(df['date'])
    
    # Create the 'cst' column with the format "DayOfWeek MM/DD/YYYY"
    # %a: Abbreviated weekday name (e.g., Sat, Sun)
    # %m: Month as zero-padded decimal number
    # %d: Day of the month as zero-padded decimal number
    # %Y: Year with century as a decimal number
    df['cst'] = df['parsed_date'].dt.strftime('%a %m/%d/%Y')
    
    # Define the mapping for renaming value columns to time columns
    # value1 -> 1:00, value2 -> 2:00, ..., value24 -> 24:00
    rename_dict = {f'value{i}': f'{i}:00' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # Define the list of columns to keep in the final output
    time_columns = [f'{i}:00' for i in range(1, 25)]
    output_columns = ['cst'] + time_columns
    
    # Sort the dataframe by the parsed date to ensure chronological order
    df = df.sort_values(by='parsed_date')
    
    # Select only the required columns
    result = df[output_columns]
    
    # Reset index to ensure a clean 0-based integer index
    result = result.reset_index(drop=True)
    
    return result
