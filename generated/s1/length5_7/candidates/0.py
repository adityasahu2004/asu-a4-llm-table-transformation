import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms sparse bi-weekly time series data into a dense daily time series
    by linear interpolation.
    """
    # 1. Parse dates and set as index
    df = source.copy()
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df = df.set_index('Date')
    
    # 2. Sort by date to ensure correct interpolation order
    df = df.sort_index()
    
    # 3. Identify numeric columns to interpolate (columns 1-24)
    # The source columns are named '1', '2', ..., '24'
    numeric_cols = [str(i) for i in range(1, 25)]
    
    # 4. Create a daily date range covering the source data
    # We use the min and max dates from the source to define the range.
    # This assumes the source data covers the period required for the target.
    start_date = df.index.min()
    end_date = df.index.max()
    
    # Create daily frequency index
    daily_index = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 5. Reindex to daily frequency
    df_daily = df.reindex(daily_index)
    
    # 6. Interpolate numeric columns linearly
    # This fills in the gaps between the bi-weekly observations
    df_daily[numeric_cols] = df_daily[numeric_cols].interpolate(method='linear')
    
    # 7. Rename columns to match target schema
    rename_map = {str(i): f'value{i}' for i in range(1, 25)}
    df_daily = df_daily.rename(columns=rename_map)
    
    # 8. Format the date index to string and reset index
    df_daily.index = df_daily.index.strftime('%Y-%m-%d 00:00:00')
    df_daily = df_daily.reset_index()
    
    # 9. Rename the index column to 'date'
    df_daily = df_daily.rename(columns={'Date': 'date'})
    
    # 10. Ensure column order matches target
    # Target columns: date, value1, ..., value24
    cols = ['date'] + [f'value{i}' for i in range(1, 25)]
    df_daily = df_daily[cols]
    
    return df_daily
