import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map source column names to 24-hour format integers
    hour_map = {
        '1:00 AM': 1, '2:00 AM': 2, '3:00 AM': 3, '4:00 AM': 4, '5:00 AM': 5, '6:00 AM': 6,
        '7:00 AM': 7, '8:00 AM': 8, '9:00 AM': 9, '10:00 AM': 10, '11:00 AM': 11,
        '12:00 AM': 12,
        '1:00 PM': 13, '2:00 PM': 14, '3:00 PM': 15, '4:00 PM': 16, '5:00 PM': 17,
        '6:00 PM': 18, '7:00 PM': 19, '8:00 PM': 20, '9:00 PM': 21, '10:00 PM': 22,
        '11:00 PM': 23, '12:00 PM': 24
    }

    # Parse dates to get month information
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    months = dates.dt.month

    # Initialize result data structure
    # We want 24 rows (hours 1-24) and 12 columns (months 1-12)
    result_data = {}
    
    for src_col, hour_int in hour_map.items():
        if src_col in source.columns:
            values = source[src_col]
            # Group by month and calculate mean
            # We need to align values with months
            series = pd.Series(values.values, index=months)
            # Calculate mean for each month (1-12)
            monthly_means = series.groupby(level=0).mean()
            # Store in result data keyed by hour_int
            result_data[hour_int] = monthly_means

    # Construct the final DataFrame
    # Create an empty dataframe with index 1-24
    df_result = pd.DataFrame(index=range(1, 25))
    df_result.index.name = 'hour'
    
    month_names = ['january', 'february', 'march', 'april', 'may', 'june', 
                   'july', 'august', 'september', 'october', 'november', 'december']
    
    for i, month_name in enumerate(month_names):
        month_num = i + 1
        # Collect values for this month across all hours
        col_values = []
        for hour_int in range(1, 25):
            if hour_int in result_data:
                # Get mean for this specific month, NaN if not present
                val = result_data[hour_int].get(month_num, np.nan)
                col_values.append(val)
            else:
                col_values.append(np.nan)
        df_result[month_name] = col_values

    # Reset index to make 'hour' a column
    df_result = df_result.reset_index()
    
    # Ensure correct column order: hour, then months
    cols = ['hour'] + month_names
    df_result = df_result[cols]
    
    return df_result
