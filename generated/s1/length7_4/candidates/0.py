import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse dates
    source = source.copy()
    source['date_dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # 2. Extract month name and daytype
    # Month name
    source['month_name'] = source['date_dt'].dt.strftime('%B')
    
    # Day type: 5=Saturday, 6=Sunday
    source['daytype'] = np.where(
        source['date_dt'].dt.dayofweek.isin([5, 6]), 
        'weekend', 
        'weekday'
    )
    
    # 3. Rename value columns to hr1...hr24
    rename_map = {f'value{i}': f'hr{i}' for i in range(1, 25)}
    source = source.rename(columns=rename_map)
    
    # 4. Group by month_name and daytype, and calculate mean for hr columns
    hr_cols = [f'hr{i}' for i in range(1, 25)]
    
    grouped = source.groupby(['month_name', 'daytype'])[hr_cols].mean()
    
    # 5. Format month string to match target (Left aligned, padded to 9 chars)
    # Target distinct values: "January  ", "February ", "March    ", etc.
    # All seem to be 9 characters long.
    result = grouped.reset_index()
    result['month'] = result['month_name'].str.ljust(9)
    
    # 6. Select and order columns
    final_cols = ['month', 'daytype'] + hr_cols
    result = result[final_cols]
    
    # Ensure dtypes are float64 for hr columns (mean might produce float64 already, but ensure)
    for col in hr_cols:
        result[col] = result[col].astype('float64')
        
    return result
