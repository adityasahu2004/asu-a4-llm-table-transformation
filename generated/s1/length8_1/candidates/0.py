import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source dataframe by aggregating cerc_logger_1 values
    by Hour and Month, then pivoting to a wide format.
    """
    # 1. Parse the date column
    # Format observed: "7/28/2019 4:50" -> %m/%d/%Y %H:%M
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    df['Hour'] = df['datetime'].dt.hour
    df['MonthNum'] = df['datetime'].dt.month
    
    # 3. Map Month numbers to names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['MonthName'] = df['MonthNum'].map(month_map)
    
    # 4. Aggregate by Hour and MonthName
    # Calculate the mean of cerc_logger_1
    agg_df = df.groupby(['Hour', 'MonthName'])['cerc_logger_1'].mean().reset_index()
    
    # 5. Pivot the table
    # Index: Hour, Columns: MonthName, Values: cerc_logger_1
    pivot_df = agg_df.pivot(index='Hour', columns='MonthName', values='cerc_logger_1')
    
    # 6. Format the output
    # Reset index to bring Hour back as a column
    result = pivot_df.reset_index()
    
    # Ensure Hour is integer
    result['Hour'] = result['Hour'].astype('int64')
    
    # Define the expected column order
    expected_months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Ensure all month columns exist (in case some are missing from data)
    for month in expected_months:
        if month not in result.columns:
            result[month] = np.nan
            
    # Select and order columns
    final_columns = ['Hour'] + expected_months
    result = result[final_columns]
    
    # Sort by Hour to ensure deterministic order
    result = result.sort_values('Hour').reset_index(drop=True)
    
    return result
