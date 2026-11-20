import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the Date column
    df = source.copy()
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Create the 'cst' column with the specific format: "DayOfWeek MM/DD/YYYY"
    # %a gives abbreviated weekday name (e.g., Tue)
    df['cst'] = df['Date'].dt.strftime('%a %m/%d/%Y')
    
    # 3. Prepare the numeric columns
    # Source columns are '1' through '24'
    numeric_cols = [str(i) for i in range(1, 25)]
    
    # 4. Select the required columns: 'cst' and the numeric ones
    # We drop 'Class' and the original 'Date'
    result = df[['cst'] + numeric_cols].copy()
    
    # 5. Rename numeric columns to '1:00', '2:00', ..., '24:00'
    new_col_names = {str(i): f"{i}:00" for i in range(1, 25)}
    result = result.rename(columns=new_col_names)
    
    # 6. Sort by the underlying date to match the target order (ascending)
    # We can sort by the 'cst' string if it's sortable, but safer to use the datetime
    # However, 'cst' is the only date-like column left. 
    # Let's add a temporary sort key or sort by 'cst' if it works.
    # "Tue 01/01/2013" vs "Thu 01/17/2013". String sort might fail if months/days aren't zero-padded consistently in a way that sorts correctly?
    # MM/DD/YYYY is zero-padded in the format string? 
    # pd.to_datetime('7/3/2013') -> 2013-07-03. 
    # strftime('%m/%d/%Y') -> '07/03/2013'.
    # The target sample shows '01/01/2013'.
    # String sorting of "Tue 01/01/2013" works if the date part is ISO-like or consistent.
    # MM/DD/YYYY is not ISO (YYYY-MM-DD). 
    # "01/01/2013" < "01/17/2013" < "02/03/2013".
    # But "Tue" vs "Thu". 
    # It is safer to sort by the original datetime before dropping it, or reconstruct it.
    
    # Let's sort by the 'cst' column? 
    # Actually, let's just sort by the index if the source was ordered, or better:
    # We can sort by the 'cst' string if we assume the format is consistent.
    # But to be robust, let's sort by the datetime value we parsed.
    
    # Re-attach datetime for sorting
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df = df.sort_values('Date')
    
    # Now select and rename
    result = df[['cst'] + numeric_cols].copy()
    result = result.rename(columns=new_col_names)
    
    # Reset index to clean up
    result = result.reset_index(drop=True)
    
    return result
