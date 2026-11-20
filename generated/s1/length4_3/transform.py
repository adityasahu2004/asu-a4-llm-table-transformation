import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame by aggregating hourly percentages by date
    and renaming columns to match the target schema.
    """
    # 1. Parse the date column
    df = source.copy()
    df['DT_STRATA'] = pd.to_datetime(df['DT_STRATA'], format='%m/%d/%Y')
    
    # 2. Identify hourly columns
    hourly_cols = [col for col in df.columns if col.startswith('PCT_HOURLY_')]
    
    # 3. Group by date and calculate the mean for each hourly column
    # We group by the parsed date. Since we want one row per date, we aggregate.
    # The target has 366 distinct dates, matching the distinct dates in source.
    # We assume the transformation is an average across all strata/rows for that day.
    grouped = df.groupby('DT_STRATA')[hourly_cols].mean()
    
    # 4. Define the mapping from source column names to target column names
    # Source: PCT_HOURLY_0100 ... PCT_HOURLY_2400
    # Target: 1:00 AM ... 12:00 PM
    
    # Mapping logic based on target column order:
    # 0100 -> 1:00 AM
    # 0200 -> 2:00 AM
    # ...
    # 1100 -> 11:00 AM
    # 1200 -> 12:00 AM  (Note: Target uses 12:00 AM for Noon position)
    # 1300 -> 1:00 PM
    # ...
    # 2300 -> 11:00 PM
    # 2400 -> 12:00 PM  (Note: Target uses 12:00 PM for Midnight position)
    
    col_mapping = {}
    for h in range(1, 25):
        src_col = f"PCT_HOURLY_{h:04d}"
        if h == 12:
            tgt_col = "12:00 AM"
        elif h == 24:
            tgt_col = "12:00 PM"
        elif h < 12:
            tgt_col = f"{h}:00 AM"
        else:
            tgt_col = f"{h-12}:00 PM"
        col_mapping[src_col] = tgt_col
        
    # Rename columns
    grouped = grouped.rename(columns=col_mapping)
    
    # 5. Format the date index to string MM/DD/YYYY
    grouped.index = grouped.index.strftime('%m/%d/%Y')
    
    # 6. Reset index to make date a column
    result = grouped.reset_index()
    
    # 7. Rename the date column to 'date'
    result = result.rename(columns={'DT_STRATA': 'date'})
    
    # 8. Sort by date to match target sample order (chronological)
    # Convert to datetime for sorting, then back to string if necessary, 
    # but since we formatted as MM/DD/YYYY, string sort might not work perfectly for all years,
    # but here all are 2016. To be safe, sort by the original datetime logic or just rely on the fact
    # that the target sample is sorted. The target distinct values start 01/01/2016.
    # Let's sort by the date string assuming YYYY is constant or parse again for sort.
    # Actually, simpler: sort by the index before resetting if we kept it as datetime.
    # We already reset. Let's sort by 'date' column.
    # Since format is MM/DD/YYYY, lexicographical sort works if year is same.
    # If years differ, we should parse.
    result['date_dt'] = pd.to_datetime(result['date'], format='%m/%d/%Y')
    result = result.sort_values('date_dt').drop(columns=['date_dt']).reset_index(drop=True)
    
    # 9. Select and order columns exactly as target
    target_cols = ['date'] + [f"{h}:00 {'AM' if h < 12 or h == 12 else 'PM'}" for h in range(1, 25)]
    # Wait, the list comprehension above is tricky for 12. Let's use the explicit list from target schema.
    target_cols = [
        'date',
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM',
        '12:00 AM',
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM',
        '12:00 PM'
    ]
    
    result = result[target_cols]
    
    return result
