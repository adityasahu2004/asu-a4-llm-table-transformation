import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['parsed_dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    df['date_only'] = df['parsed_dt'].dt.date
    df['hour'] = df['parsed_dt'].dt.hour + 1 # 1-based hour
    
    # Pivot the data
    # We need to handle potential duplicates if any, though likely unique per hour
    # Using pivot_table with aggfunc='last' or similar if duplicates exist
    # The source has 15117 rows, target has 53 rows. 
    # 53 days * 24 hours = 1272. 15117 / 53 is roughly 285. 
    # Wait, 15117 rows in source? And 53 in target?
    # The source sample shows 12 rows. The target sample shows 12 rows.
    # The distinct count of dates in source is 15117? No, distinct is 15117 for 'date' column?
    # "distinct": 15117 for 'date'. This means every row has a unique timestamp.
    # Target has 53 rows. 
    # 15117 / 53 is approx 285. This doesn't divide evenly.
    # Let's look at the source distinct values for zone_016_cooling_sp: 73.0, 84.0, null.
    # The target has 53 distinct dates.
    # Perhaps the source contains many measurements per day, and we are aggregating?
    # Or perhaps the source contains measurements for many zones, but we only see one column?
    # The column name is zone_016_cooling_sp.
    # If there are 15117 unique timestamps, and we end up with 53 dates, 
    # then there are ~285 measurements per day on average.
    # The target has 24 hours. 
    # So for each date, we have 24 values.
    # How do we get 24 values from ~285 measurements?
    # Maybe we take the value at the specific hour?
    # But the timestamps are like "21:45", "16:15". They are not on the hour.
    # However, the target columns are "Hour 1", "Hour 2", etc.
    # Usually, this implies bucketing by hour.
    # If multiple measurements fall in the same hour, we might need to average or take last?
    # Given the values are mostly 73.0, and some 84.0, and the target is all 73.0 (except nulls),
    # it's likely that for the target dates, the value was consistently 73.0.
    # Let's assume we group by date and hour, and take the mean or last value.
    # Given the simplicity, let's try taking the last value or mean.
    # But wait, look at the target nulls. Hours 1-9 and 22-24 have nulls. Hours 10-21 do not.
    # This pattern suggests that for some hours, there was no data?
    # If we simply group by date and hour, and take the mean, we might get values.
    
    # Let's refine the grouping.
    # df['hour'] is 1-24.
    # We group by 'date_only' and 'hour'.
    # We aggregate 'zone_016_cooling_sp'.
    
    grouped = df.groupby(['date_only', 'hour'])['zone_016_cooling_sp'].last()
    
    # Unpivot to wide format
    pivoted = grouped.unstack('hour')
    
    # Ensure all 24 hours are present
    all_hours = range(1, 25)
    pivoted = pivoted.reindex(columns=all_hours)
    
    # Rename columns
    pivoted.columns = [f'Hour {h}' for h in all_hours]
    
    # Reset index
    pivoted = pivoted.reset_index()
    
    # Format date
    pivoted['date'] = pivoted['date_only'].dt.strftime('%m/%d/%Y')
    pivoted = pivoted.drop(columns=['date_only'])
    
    # Reorder columns to match target: date, Hour 1, ..., Hour 24
    cols = ['date'] + [f'Hour {h}' for h in range(1, 25)]
    pivoted = pivoted[cols]
    
    # Cast dtypes: int if no nulls, else float
    for col in [f'Hour {h}' for h in range(1, 25)]:
        if pivoted[col].isnull().any():
            pivoted[col] = pivoted[col].astype('float64')
        else:
            pivoted[col] = pivoted[col].astype('int64')
            
    return pivoted.reset_index(drop=True)
