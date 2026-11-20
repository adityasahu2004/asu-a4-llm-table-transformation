import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from a wide format with AM/PM hour columns
    to a target format with 24-hour columns (1:00 to 24:00) and a formatted date column.
    """
    
    # 1. Melt the DataFrame to long format
    # Keep 'date' as id, drop 'DSL' as it's not in the target
    id_cols = ['date']
    value_cols = [col for col in source.columns if col not in id_cols and col != 'DSL']
    
    melted = pd.melt(
        source, 
        id_vars=id_cols, 
        value_vars=value_cols, 
        var_name='time_label', 
        value_name='value'
    )
    
    # 2. Parse time labels to 24-hour integer format
    # Mapping:
    # 12:00 AM -> 24
    # 1:00 AM  -> 1
    # ...
    # 11:00 AM -> 11
    # 12:00 PM -> 12
    # 1:00 PM  -> 13
    # ...
    # 11:00 PM -> 23
    
    def parse_hour(label):
        # Split by space to get time and AM/PM
        parts = label.split()
        time_part = parts[0]
        ampm = parts[1]
        
        hour_str, minute_str = time_part.split(':')
        hour = int(hour_str)
        
        if ampm == 'AM':
            if hour == 12:
                return 24
            else:
                return hour
        else: # PM
            if hour == 12:
                return 12
            else:
                return hour + 12
                
    melted['hour'] = melted['time_label'].apply(parse_hour)
    
    # 3. Pivot back to wide format
    # Index: date, Columns: hour, Values: value
    pivoted = melted.pivot(index='date', columns='hour', values='value')
    
    # 4. Reset index to make 'date' a column
    pivoted = pivoted.reset_index()
    
    # 5. Format the date column to 'cst'
    # Source format: "M/D/YYYY" (e.g., "7/3/2014")
    # Target format: "DayOfWeek MM/DD/YYYY" (e.g., "Wed 01/01/2014")
    
    # Parse the date string
    pivoted['date_dt'] = pd.to_datetime(pivoted['date'], format='%m/%d/%Y')
    
    # Format to target string
    pivoted['cst'] = pivoted['date_dt'].dt.strftime('%a %m/%d/%Y')
    
    # Drop the original date and datetime helper columns
    pivoted = pivoted.drop(columns=['date', 'date_dt'])
    
    # 6. Rename hour columns to "H:00" format
    # The columns are integers 1 to 24
    new_col_names = {}
    for col in pivoted.columns:
        if col != 'cst':
            new_col_names[col] = f"{int(col)}:00"
            
    pivoted = pivoted.rename(columns=new_col_names)
    
    # 7. Ensure column order: 'cst' followed by 1:00 to 24:00
    # The pivot columns might not be sorted if the source wasn't, but pivot usually sorts.
    # Let's explicitly order them.
    
    ordered_cols = ['cst'] + [f"{h}:00" for h in range(1, 25)]
    
    # Select only the columns that exist (in case some hours are missing in source, though unlikely)
    # The problem implies a complete set.
    result = pivoted[ordered_cols]
    
    # Sort by date if necessary? The target sample is sorted by date.
    # It's good practice to sort by the date column.
    # We need to parse 'cst' again or use the original date for sorting.
    # Let's create a temporary datetime for sorting.
    sort_df = result.copy()
    sort_df['sort_key'] = pd.to_datetime(sort_df['cst'], format='%a %m/%d/%Y')
    result = result.sort_values(by='sort_key').reset_index(drop=True)
    result = result.drop(columns=['sort_key'])
    
    return result
