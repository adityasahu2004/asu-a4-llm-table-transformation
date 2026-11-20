import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date string
    # Format: M/d/yyyy H:mm
    source = source.copy()
    source['parsed_dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y %I:%M %p')
    
    # Handle cases where AM/PM might be missing or format is slightly different
    # The sample shows "4:50", "9:30", "18:50". 
    # "18:50" implies 24-hour format. "4:50" could be 4:50 AM.
    # Let's look at the sample: "1/1/2021 0:00". This is 24-hour format.
    # "11/2/2019 18:50". This is 24-hour format.
    # So the format is likely '%m/%d/%Y %H:%M'.
    
    # Re-parse with 24-hour format
    source['parsed_dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract calendar date and hour
    source['cal_date'] = source['parsed_dt'].dt.date
    source['hour'] = source['parsed_dt'].dt.hour
    
    # 3. Aggregate by date and hour
    # We need to group by calendar date and hour, then mean the values
    agg_df = source.groupby(['cal_date', 'hour'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot to wide format
    # Index: cal_date, Columns: hour, Values: cerc_logger_1
    pivot_df = agg_df.pivot(index='cal_date', columns='hour', values='cerc_logger_1')
    
    # 5. Rename columns from 0-23 to "Hour 1" - "Hour 24"
    pivot_df.columns = [f'Hour {h+1}' for h in pivot_df.columns]
    
    # 6. Sort columns by hour number to ensure correct order
    # The column names are "Hour 1", "Hour 2", ... "Hour 24"
    # Sorting them lexicographically might fail for "Hour 10" vs "Hour 2".
    # But we generated them in order. Let's ensure they are in order 1-24.
    pivot_df = pivot_df[[f'Hour {h}' for h in range(1, 25)]]
    
    # 7. Reset index to make date a column
    result = pivot_df.reset_index()
    
    # 8. Format date as MM/DD/YYYY
    result['date'] = pd.to_datetime(result['cal_date']).dt.strftime('%m/%d/%Y')
    
    # 9. Drop the helper column if it exists (cal_date is now index or dropped)
    # Since we reset index, 'cal_date' is now a column named 'cal_date' or 'date' if we renamed?
    # In step 7, reset_index() creates a column from the index. The index name was 'cal_date'.
    # So the column is 'cal_date'. We want it to be 'date'.
    
    result = result.rename(columns={'cal_date': 'date'})
    
    # Select only the required columns
    final_cols = ['date'] + [f'Hour {h}' for h in range(1, 25)]
    result = result[final_cols]
    
    return result
