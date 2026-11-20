import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source electricity rate DataFrame into the target format.
    
    Operations:
    1. Parses the 'Date' column.
    2. Formats the date into 'cst' column as "DayOfWeek MM/DD/YYYY".
    3. Renames 'Hr X' columns to 'X:00'.
    4. Selects and orders columns to match target schema.
    """
    # Create a copy to avoid modifying the original source
    df = source.copy()
    
    # 1. Parse the Date column
    # The source format is M/D/YYYY (e.g., "1/1/2014")
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Create the 'cst' column with format "Wed 01/01/2014"
    # %a = Abbreviated weekday name (e.g., Wed)
    # %m = Month as zero-padded decimal number
    # %d = Day of the month as zero-padded decimal number
    # %Y = Year with century as a decimal number
    df['cst'] = df['Date'].dt.strftime('%a %m/%d/%Y')
    
    # 3. Rename Hour columns from "Hr X" to "X:00"
    # Generate mapping for hours 1 to 24
    rename_map = {f'Hr {i}': f'{i}:00' for i in range(1, 25)}
    df.rename(columns=rename_map, inplace=True)
    
    # 4. Select and order columns
    # Target columns: 'cst', '1:00', '2:00', ..., '24:00'
    target_cols = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # Ensure all target columns exist (they should based on schema)
    result = df[target_cols]
    
    return result
