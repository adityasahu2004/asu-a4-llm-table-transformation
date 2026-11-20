import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # 1. dt_strata: Format as M/D/YYYY
    # Note: Target sample shows "1/1/2011", implying no leading zeros for month/day if single digit.
    # However, standard strftime %m/%d/%Y produces leading zeros (01/01/2011).
    # Looking closely at target sample: "1/1/2011", "1/17/2011", "2/3/2011".
    # This suggests stripping leading zeros.
    # Let's try standard format first, but the sample explicitly lacks leading zeros.
    # To be safe and match "1/1/2011", we can use %m/%d/%Y and replace leading zeros, 
    # or use a custom formatter. 
    # Actually, looking at "7/2/2011" in source vs "1/1/2011" in target.
    # Let's use strftime and strip leading zeros from month and day.
    dt_strata_formatted = dates.dt.strftime('%m/%d/%Y').str.lstrip('0').str.replace('/0', '/', regex=False)
    # Correction: str.lstrip('0') on "01/01/2011" -> "1/1/2011" works? 
    # "01/01/2011".lstrip('0') -> "1/1/2011". 
    # "10/01/2011".lstrip('0') -> "10/1/2011". 
    # "01/10/2011".lstrip('0') -> "1/10/2011".
    # This simple lstrip might fail if day is 10-31? No, lstrip only removes from start.
    # But "01/01/2011" -> "1/1/2011". 
    # What about "01/10/2011"? -> "1/10/2011". Correct.
    # What about "10/01/2011"? -> "10/1/2011". Correct.
    # So str.lstrip('0') on the whole string is risky if the string starts with 0 but we want to keep 0 in middle?
    # No, lstrip only affects the beginning. 
    # Wait, "01/01/2011".lstrip('0') is "1/1/2011".
    # "09/01/2011".lstrip('0') is "9/1/2011".
    # This seems correct for the pattern M/D/YYYY.
    out['dt_strata'] = dt_strata_formatted

    # 2. dow: ISO day of week (1=Mon, 7=Sun)
    out['dow'] = dates.dt.dayofweek + 1

    # 3. Hourly columns mapping
    for h in range(1, 25):
        src_col = f'value{h}'
        tgt_col = f'pct_hourly_{h:02d}00'
        out[tgt_col] = source[src_col]

    # 4. Constant column
    out['pct_hourly_2500'] = 0

    return out.reset_index(drop=True)
