import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    dt = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    months = dt.dt.month
    
    # Mapping for month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    results = []
    
    for h in range(1, 25):
        col_name = f'PCT_HOURLY_{h:02d}00'
        
        # Calculate mean for each month for this hour
        hourly_data = source[col_name]
        
        # Group by month and calculate mean
        # We need to align the months with the rows
        grouped = pd.Series(hourly_data.values, index=months).groupby(months).mean()
        
        row = {'hour': h}
        for m, name in month_names.items():
            if m in grouped.index:
                row[name] = grouped[m]
            else:
                row[name] = np.nan # Should not happen given data coverage, but safe to handle
        
        results.append(row)
        
    target_df = pd.DataFrame(results)
    
    # Ensure correct column order
    cols = ['hour'] + [month_names[m] for m in range(1, 13)]
    target_df = target_df[cols]
    
    # Ensure dtypes
    target_df['hour'] = target_df['hour'].astype(int)
    for col in cols[1:]:
        target_df[col] = target_df[col].astype(float)
        
    return target_df
