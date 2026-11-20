import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date to extract month
    source['parsed_date'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month'] = source['parsed_date'].dt.month
    
    # Define target columns
    month_cols = [
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # Initialize result dataframe with hour column
    res = pd.DataFrame({'hour': range(1, 25)})
    
    # Calculate mean for each hour for each month
    # We group by month, then for each group, we take the mean of the hour columns
    grouped = source.groupby('month')
    
    for i, month_name in enumerate(month_cols, start=1):
        if i in grouped.groups:
            month_data = grouped.get_group(i)
            # Select hour columns
            hour_cols = [f'Hour {h}' for h in range(1, 25)]
            # Calculate mean for each hour column
            means = month_data[hour_cols].mean()
            # Assign to the result dataframe
            res[month_name] = means.values
        else:
            # If month not present, fill with NaN
            res[month_name] = np.nan
            
    return res
