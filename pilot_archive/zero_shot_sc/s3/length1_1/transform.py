import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame to match the target schema.
    
    Operations:
    1. Parses DT_STRATA to datetime.
    2. Formats date to 'Day MM/DD/YYYY' string for column 'cst'.
    3. Renames PCT_HOURLY_XX00 columns to XX:00 format.
    4. Selects and orders columns as per target schema.
    """
    
    # 1. Parse the date column
    # The format M/D/YYYY can be handled by pandas to_datetime
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['DT_STRATA'], format='%m/%d/%Y')
    
    # 2. Format the date string for the 'cst' column
    # Target format: "Fri 01/01/2016" -> %a %m/%d/%Y
    # Note: %a gives locale's abbreviated weekday name (e.g., Fri, Sun)
    df['cst'] = df['parsed_date'].dt.strftime('%a %m/%d/%Y')
    
    # 3. Rename hourly columns
    # Source: PCT_HOURLY_0100, ..., PCT_HOURLY_2400
    # Target: 1:00, ..., 24:00
    
    rename_map = {}
    for col in df.columns:
        if col.startswith('PCT_HOURLY_') and col.endswith('00'):
            # Extract the middle part, e.g., '01' from 'PCT_HOURLY_0100'
            hour_str = col.replace('PCT_HOURLY_', '').replace('00', '')
            # Convert to int to remove leading zeros for the key, but we need to format it
            # Actually, the target is "1:00", "10:00". 
            # Source "PCT_HOURLY_0100" -> Hour 1 -> "1:00"
            # Source "PCT_HOURLY_1000" -> Hour 10 -> "10:00"
            try:
                hour_int = int(hour_str)
                new_col_name = f"{hour_int}:00"
                rename_map[col] = new_col_name
            except ValueError:
                pass
                
    df.rename(columns=rename_map, inplace=True)
    
    # 4. Select and order columns
    # Target columns: cst, 1:00, 2:00, ..., 24:00
    target_cols = ['cst'] + [f"{h}:00" for h in range(1, 25)]
    
    # Filter to ensure only requested columns are present and in order
    # Check if columns exist to avoid errors if data is missing
    existing_target_cols = [col for col in target_cols if col in df.columns]
    
    result = df[existing_target_cols]
    
    # Clean up temporary column
    if 'parsed_date' in result.columns:
        result.drop(columns=['parsed_date'], inplace=True)
        
    return result
