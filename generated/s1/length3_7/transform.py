import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms bi-weekly hourly load data into daily hourly load data by:
    1. Parsing dates and creating a daily frequency index.
    2. Interpolating missing daily values.
    3. Renaming columns to match the target schema.
    4. Formatting dates as MM/DD/YYYY strings.
    """
    # 1. Parse the Date column
    df = source.copy()
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # Set Date as index for time-series operations
    df = df.set_index('Date')
    
    # 2. Define the full daily date range
    # Determine the start and end of the range based on source data
    start_date = df.index.min()
    end_date = df.index.max()
    
    # Create a daily frequency date range
    daily_index = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 3. Reindex to daily frequency and interpolate
    # We drop the 'Class' column as it's not in the target and is constant
    df_numeric = df.drop(columns=['Class'], errors='ignore')
    
    # Reindex to daily frequency. This introduces NaNs for missing days.
    df_daily = df_numeric.reindex(daily_index)
    
    # Interpolate linearly to fill the gaps between bi-weekly snapshots
    # axis=0 interpolates down the rows (time)
    df_daily = df_daily.interpolate(method='linear')
    
    # 4. Rename columns
    # Map '1'...'24' to 'Hour 1'...'Hour 24'
    rename_map = {str(i): f"Hour {i}" for i in range(1, 25)}
    df_daily = df_daily.rename(columns=rename_map)
    
    # 5. Format the date index back to a column
    df_daily = df_daily.reset_index()
    df_daily = df_daily.rename(columns={'index': 'date'})
    
    # Format date as MM/DD/YYYY string
    df_daily['date'] = df_daily['date'].dt.strftime('%m/%d/%Y')
    
    # 6. Ensure column order matches target
    # Target columns: date, Hour 1, ..., Hour 24
    target_cols = ['date'] + [f"Hour {i}" for i in range(1, 25)]
    df_daily = df_daily[target_cols]
    
    return df_daily
