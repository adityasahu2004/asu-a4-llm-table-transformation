import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms sparse hourly load data into a dense daily time series with interpolated values.
    """
    # 1. Parse the date column
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Set date as index and sort to ensure proper interpolation
    df = df.set_index('date').sort_index()
    
    # 3. Identify value columns
    value_cols = [f'value{i}' for i in range(1, 25)]
    
    # 4. Generate a complete date range from min to max date in the source
    # The target has 183 rows, source has 182. The range likely covers the full span.
    # We create a daily frequency range.
    min_date = df.index.min()
    max_date = df.index.max()
    full_date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    
    # 5. Reindex to the full date range to introduce NaNs for missing days
    df = df.reindex(full_date_range)
    
    # 6. Interpolate the value columns linearly
    # Using linear interpolation on the datetime index
    df[value_cols] = df[value_cols].interpolate(method='time')
    
    # 7. Create the 'cst' column with the specific format: "DayOfWeek MM/DD/YYYY"
    # Example: "Sat 01/01/2011"
    # %a gives abbreviated weekday (Sat), %m gives zero-padded month, %d zero-padded day, %Y 4-digit year
    df['cst'] = df.index.strftime('%a %m/%d/%Y')
    
    # 8. Rename value columns to hour format "H:00"
    rename_map = {f'value{i}': f'{i}:00' for i in range(1, 25)}
    df = df.rename(columns=rename_map)
    
    # 9. Select and order columns as per target schema
    # Target columns: cst, 1:00, 2:00, ..., 24:00
    hour_cols = [f'{i}:00' for i in range(1, 25)]
    final_cols = ['cst'] + hour_cols
    
    result = df[final_cols].reset_index(drop=True)
    
    return result
