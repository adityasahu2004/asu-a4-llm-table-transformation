import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    source = source.copy()
    source['DT_STRATA'] = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    
    # 2. Identify hourly columns to aggregate
    # Source columns: PCT_HOURLY_0100 to PCT_HOURLY_2400
    hourly_cols = [f'PCT_HOURLY_{h:04d}' for h in range(1, 25)]
    
    # 3. Group by date and calculate mean
    # We group by the parsed datetime object
    grouped = source.groupby(source['DT_STRATA'])[hourly_cols].mean()
    
    # 4. Reset index to make date a column
    result = grouped.reset_index()
    
    # 5. Format the date column as "DayName MM/DD/YYYY"
    # e.g., "Fri 01/01/2016"
    # %a gives abbreviated weekday name (e.g., Fri)
    # %m/%d/%Y gives MM/DD/YYYY
    result['cst'] = result['DT_STRATA'].dt.strftime('%a %m/%d/%Y')
    
    # 6. Rename hourly columns to "1:00", "2:00", ..., "24:00"
    rename_map = {f'PCT_HOURLY_{h:04d}': f'{h:02d}:00' if h < 10 else f'{h}:00' 
                  for h in range(1, 25)}
    # Wait, target names are "1:00", "2:00" ... "9:00", "10:00" ... "24:00"
    # The format string for hour 1 is "1:00", for 10 is "10:00".
    # Let's refine the rename map keys to match source and values to match target.
    
    rename_map = {}
    for h in range(1, 25):
        src_col = f'PCT_HOURLY_{h:04d}'
        tgt_col = f'{h}:00'
        rename_map[src_col] = tgt_col
        
    result = result.rename(columns=rename_map)
    
    # 7. Select and order columns
    # Target columns: cst, 1:00, 2:00, ..., 24:00
    target_cols = ['cst'] + [f'{h}:00' for h in range(1, 25)]
    result = result[target_cols]
    
    # 8. Sort by date to match typical chronological order (optional but good practice)
    # The target sample is not strictly sorted by date (Fri 01/01, Sun 05/29, Wed 10/26...), 
    # but usually transformations preserve some order or sort. 
    # Given the target sample looks random or specific, we should probably just return the grouped result.
    # However, groupby usually sorts by the key. Let's sort by the original date to be deterministic.
    # We can sort by the 'cst' string if we parse it, but easier to sort by the index before reset or keep the datetime.
    # Let's add the datetime back temporarily to sort, or just sort by 'cst' if it parses correctly?
    # "Fri 01/01/2016" -> standard sort might not work chronologically if day names vary length? 
    # Actually, let's just sort by the underlying date.
    
    # Re-parse cst to datetime for sorting? Or just rely on the groupby order.
    # groupby sorts by key by default. So the result is sorted by date.
    
    return result
