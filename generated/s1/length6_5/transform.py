import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame by:
    1. Parsing dates.
    2. Renaming numeric columns to 'Hr X'.
    3. Generating a complete daily date range to fill missing days.
    4. Interpolating values for missing days.
    5. Formatting dates to MM/DD/YYYY.
    """
    # 1. Parse Date column
    df = source.copy()
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Rename columns 1-24 to Hr 1 - Hr 24
    rename_map = {str(i): f'Hr {i}' for i in range(1, 25)}
    df.rename(columns=rename_map, inplace=True)
    
    # 3. Identify date range and create complete index
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    
    # Create a complete daily date range
    full_date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    
    # 4. Set Date as index and reindex to fill missing days
    df_indexed = df.set_index('Date')
    df_reindexed = df_indexed.reindex(full_date_range)
    
    # 5. Interpolate missing values (for the missing day)
    # The target has no nulls, so we interpolate linearly across the hourly columns
    # We select only the numeric columns for interpolation
    numeric_cols = [f'Hr {i}' for i in range(1, 25)]
    df_reindexed[numeric_cols] = df_reindexed[numeric_cols].interpolate(method='linear')
    
    # 6. Reset index and format date
    df_result = df_reindexed.reset_index()
    df_result.rename(columns={'index': 'Date'}, inplace=True)
    
    # Format Date to MM/DD/YYYY
    df_result['Date'] = df_result['Date'].dt.strftime('%m/%d/%Y')
    
    # 7. Ensure correct column order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    df_result = df_result[target_columns]
    
    return df_result
