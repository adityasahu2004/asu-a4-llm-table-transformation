import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse dates to extract month
    source = source.copy()
    source['date_parsed'] = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    source['month'] = source['date_parsed'].dt.month
    
    # 2. Select hourly columns
    hourly_cols = [f'PCT_HOURLY_{h:02d}00' for h in range(1, 25)]
    
    # 3. Group by month and calculate mean for each hour
    # Resulting shape: 12 rows (months 1-12) x 24 columns (hours)
    agg_df = source.groupby('month')[hourly_cols].mean()
    
    # 4. Transpose to get Hours as rows and Months as columns
    # agg_df.T has index 1..24 (hours) and columns 1..12 (months)
    transposed_df = agg_df.T
    
    # 5. Rename columns to month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    transposed_df.rename(columns=month_names, inplace=True)
    
    # 6. Create the final dataframe
    result = transposed_df.reset_index()
    result.rename(columns={'index': 'hour'}, inplace=True)
    
    # Ensure hour is integer
    result['hour'] = result['hour'].astype(int)
    
    # Ensure column order matches target: hour, january, february, ...
    target_cols = ['hour'] + [month_names[i] for i in range(1, 13)]
    result = result[target_cols]
    
    return result
