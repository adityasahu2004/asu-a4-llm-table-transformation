import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Melt the dataframe to long format
    # Keep 'date' as identifier, unpivot the hour columns
    id_vars = ['date']
    value_vars = [col for col in source.columns if col not in id_vars and col != 'DSL']
    
    long_df = source.melt(id_vars=id_vars, value_vars=value_vars, var_name='hour_label', value_name='value')
    
    # 2. Map hour labels to 24-hour format integers (1-24)
    # Mapping logic:
    # 12:00 AM -> 24
    # 1:00 AM - 11:00 AM -> 1-11
    # 12:00 PM -> 12
    # 1:00 PM - 11:00 PM -> 13-23
    
    def map_hour(label):
        if 'AM' in label:
            if label.startswith('12:'):
                return 24
            else:
                return int(label.split(':')[0])
        else: # PM
            if label.startswith('12:'):
                return 12
            else:
                return int(label.split(':')[0]) + 12

    long_df['hour'] = long_df['hour_label'].apply(map_hour)
    
    # 3. Parse date and extract month
    long_df['date_dt'] = pd.to_datetime(long_df['date'], format='%m/%d/%Y')
    long_df['month'] = long_df['date_dt'].dt.month
    
    # 4. Group by hour and month, calculate mean
    # The target has one row per hour, one col per month.
    # We aggregate values for each (hour, month) pair.
    grouped = long_df.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 5. Pivot the data
    # Index: hour, Columns: month, Values: mean value
    pivoted = grouped.pivot(index='hour', columns='month', values='value')
    
    # 6. Ensure all months 1-12 are present and rename columns
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    pivoted.rename(columns=month_names, inplace=True)
    
    # Ensure all month columns exist, filling with NaN if data is missing
    for m in range(1, 13):
        if month_names[m] not in pivoted.columns:
            pivoted[month_names[m]] = np.nan
            
    # 7. Reset index and sort by hour
    pivoted.reset_index(inplace=True)
    pivoted.sort_values(by='hour', inplace=True)
    
    # 8. Select and order columns as per target
    target_cols = ['hour'] + [month_names[m] for m in range(1, 13)]
    result = pivoted[target_cols]
    
    # Ensure hour is int64
    result['hour'] = result['hour'].astype('int64')
    
    return result
