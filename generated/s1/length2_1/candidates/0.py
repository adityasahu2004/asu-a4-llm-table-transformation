import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame by:
    1. Parsing the 'CST' date column.
    2. Shifting the date back by 3 years to create 'dt_strata'.
    3. Extracting the day of the week (1=Mon, 7=Sun) for 'dow'.
    4. Renaming hourly columns from 'H:00' format to 'pct_hourly_HH00'.
    5. Rounding hourly values to 2 decimal places.
    6. Adding a constant column 'pct_hourly_2500' with value 0.
    """
    
    # 1. Parse the CST column
    # Format: "Sat 12/01/2012" -> "%a %m/%d/%Y"
    # We only need the date part for calculation, but parsing the whole string is robust.
    # Note: pd.to_datetime handles the day-of-week prefix if we specify the format correctly or let it infer.
    # Explicit format is safer.
    source['parsed_date'] = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    # 2. Calculate target date (3 years prior)
    # Using DateOffset to handle year subtraction correctly
    target_dates = source['parsed_date'] - pd.DateOffset(years=3)
    
    # Format dt_strata as MM/DD/YYYY
    dt_strata = target_dates.dt.strftime('%m/%d/%Y')
    
    # 3. Extract Day of Week (1=Monday, 7=Sunday)
    # isoweekday() returns 1 for Monday, 7 for Sunday
    dow = target_dates.dt.isoweekday().astype('int64')
    
    # 4. Process Hourly Columns
    # Source columns: '1:00', '2:00', ..., '24:00:00'
    # Target columns: 'pct_hourly_0100', ..., 'pct_hourly_2400'
    
    # Identify hourly columns (all float64 columns except potentially others, but here all non-CST are hourly)
    hourly_cols = [col for col in source.columns if col != 'CST']
    
    # Create a mapping for renaming
    # We need to parse the hour from the source column name
    # '1:00' -> 1, '24:00:00' -> 24
    
    def get_hour(col_name):
        # Remove ':00' or ':00:00' and parse int
        # Simple split by ':' and take first part
        return int(col_name.split(':')[0])
    
    # Build new dataframe for hourly data
    hourly_data = source[hourly_cols].copy()
    
    # Rename columns
    new_col_names = {}
    for col in hourly_cols:
        h = get_hour(col)
        # Format: pct_hourly_HH00
        new_name = f"pct_hourly_{h:02d}00"
        new_col_names[col] = new_name
        
    hourly_data = hourly_data.rename(columns=new_col_names)
    
    # Round to 2 decimal places as observed in target sample
    hourly_data = hourly_data.round(2)
    
    # 5. Construct Final DataFrame
    result = pd.DataFrame()
    result['dt_strata'] = dt_strata
    result['dow'] = dow
    
    # Add hourly columns in order 01 to 24
    for h in range(1, 25):
        col_name = f"pct_hourly_{h:02d}00"
        result[col_name] = hourly_data[col_name]
        
    # Add constant column
    result['pct_hourly_2500'] = 0
    
    # Ensure correct dtypes
    result['dow'] = result['dow'].astype('int64')
    result['pct_hourly_2500'] = result['pct_hourly_2500'].astype('int64')
    
    # Clean up temporary column if it was added to source (it wasn't, we used a local var)
    # But we should ensure we don't return extra columns
    return result
