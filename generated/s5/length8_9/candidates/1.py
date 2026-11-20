import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Identify hourly columns
    hr_cols = [c for c in source.columns if c.startswith('Hr ')]
    
    # 2. Parse Date and extract Month
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    months = dates.dt.month
    
    # 3. Group by Month and sum the hourly columns
    # Create a dataframe with just the month and the hourly values
    df_agg = pd.DataFrame({
        'Month': months,
        **{col: source[col] for col in hr_cols}
    })
    
    # Group by Month and sum
    grouped = df_agg.groupby('Month').sum()
    
    # 4. Transpose to get Hours as rows and Months as columns
    # grouped index is Month (1-12), columns are Hr 1-24
    transposed = grouped.T
    
    # 5. Rename columns to month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    transposed.columns = [month_names[col] for col in transposed.columns]
    
    # 6. Rename index to 'hour' and convert to integer
    # The index is currently strings like 'Hr 1', 'Hr 2'
    transposed.index = transposed.index.str.replace('Hr ', '').astype(int)
    transposed.index.name = 'hour'
    
    # 7. Reset index to make 'hour' a column
    result = transposed.reset_index()
    
    return result
