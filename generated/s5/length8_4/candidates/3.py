import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    dates = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    months = dates.dt.month
    
    # Prepare result storage
    hours = []
    monthly_vals = {m: [] for m in range(1, 13)}
    
    # Hours 1 to 24
    for h in range(1, 25):
        col_name = f'PCT_HOURLY_{h:02d}00'
        vals = source[col_name].values
        
        # Calculate mean for each month
        hour_row = [h]
        for m in range(1, 13):
            mask = months.values == m
            if np.any(mask):
                mean_val = np.mean(vals[mask])
            else:
                mean_val = np.nan
            hour_row.append(mean_val)
        
        hours.append(hour_row)
    
    # Create DataFrame
    month_names = [
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    cols = ['hour'] + month_names
    result_df = pd.DataFrame(hours, columns=cols)
    
    # Ensure correct dtypes
    result_df['hour'] = result_df['hour'].astype('int64')
    for col in month_names:
        result_df[col] = result_df[col].astype('float64')
        
    return result_df
