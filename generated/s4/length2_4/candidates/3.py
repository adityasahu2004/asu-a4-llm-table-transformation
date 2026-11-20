import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the source Date column
    # The source format is M/D/YYYY or MM/DD/YYYY
    dt_series = pd.to_datetime(source['Date'])
    
    # Create the output DataFrame
    out = pd.DataFrame()
    
    # Calculate dt_strata: Date - 1 day? 
    # The prompt samples are disjoint. However, typically these tasks imply a direct mapping.
    # If we look at the previous examples, the date was often shifted or reformatted.
    # Given the disjoint nature, and the "183 vs 182" count, it's highly probable the evaluation 
    # source will have dates that map 1-to-1 to the target dates.
    # The most robust assumption for "Infer transformation" when samples are disjoint is 
    # to apply the structural changes. 
    # Does the date change? 
    # In the previous example, Source DT_STRATA was used directly.
    # Here, Source is 'Date'. Target is 'dt_strata'.
    # If I assume 1-to-1, I should probably keep the date as is, or shift it?
    # Let's look at the DOW.
    # If I keep the date as is:
    # Source 7/3/2013 (Tue). Target DOW for Tue is 2.
    # If I shift date back 1 day:
    # Source 7/3/2013 -> 7/2/2013 (Mon). Target DOW for Mon is 1.
    # The target sample for 7/2/2013 (Mon) has DOW 2? No, 7/2/2013 is Monday.
    # Wait, 7/2/2013 is Monday. 
    # My previous analysis: 1/1/2013 (Tue) -> 2. 2/3/2013 (Sun) -> 0.
    # If 7/2/2013 is Monday, DOW should be 1.
    # Let's check the target sample for 7/2/2013.
    # The last row of target sample is 7/2/2013.
    # The DOW column for that row is 2.
    # 7/2/2013 is a Monday.
    # If Mon=1, why is DOW 2?
    # Maybe 7/2/2013 is NOT Monday?
    # 2013 is not a leap year.
    # Jan 1 2013 was Tuesday.
    # July 2 2013:
    # Jan: 31, Feb: 28, Mar: 31, Apr: 30, May: 31, Jun: 30.
    # Days from Jan 1 to Jul 2: 31+28+31+30+31+30 + 1 = 182 days.
    # 182 % 7 = 0.
    # So July 2 is the same day of week as Jan 1.
    # Jan 1 was Tuesday. So July 2 is Tuesday.
    # Ah! 7/2/2013 is Tuesday.
    # My previous mental calendar was wrong.
    # So:
    # 1/1/2013 (Tue) -> DOW 2.
    # 7/2/2013 (Tue) -> DOW 2.
    # This is consistent.
    
    # Now, does the date shift?
    # Source sample starts 7/3/2013.
    # Target sample ends 7/2/2013.
    # If the transformation is 1-to-1, and the samples are just different slices, 
    # I should check if Source Date maps to Target dt_strata directly or shifted.
    # If I assume no shift: Source 7/3/2013 (Wed) -> Target 7/3/2013 (Wed).
    # Wed DOW should be 3.
    # If I assume -1 day shift: Source 7/3/2013 -> Target 7/2/2013 (Tue).
    # Tue DOW should be 2.
    
    # Let's look at the row counts again.
    # Source: 182 rows.
    # Target: 183 rows.
    # This implies the Target has one more row than the Source.
    # This often happens if the Target includes a "previous day" or "next day" boundary.
    # Or if the Source is missing a row in the sample.
    # However, without explicit instruction to add rows, and given the "untrusted data" constraint,
    # I should stick to transforming the existing rows.
    # The discrepancy in sample sizes (182 vs 183) might be an artifact of the sample selection 
    # (e.g. target sample includes Jan 1, source sample starts later).
    # I will assume a 1-to-1 row mapping.
    
    # Regarding the date shift:
    # In many energy/load forecasting datasets, "Date" might be the billing date or 
    # the date of the record, while the load profile is for the previous day.
    # However, without clear evidence (like matching values), I will assume the date 
    # in `dt_strata` is the same as `Date` in the source, just reformatted.
    # Why? Because the target sample `7/2/2013` has values `0.66...`.
    # The source sample `7/3/2013` has values `0.56...`.
    # They are different.
    # If I look for `7/2/2013` in the source... it's not in the sample.
    # If I look for `7/3/2013` in the target... it's not in the sample.
    # I cannot verify the shift.
    # Standard practice: If not specified, keep the date.
    # BUT, the column name `dt_strata` and `dow` suggests a time-series index.
    # I will keep the date as is.
    
    # Wait, looking at the previous turn (Task 2), the source `CST` was parsed and used directly.
    # In Task 1, `DT_STRATA` was parsed and used directly.
    # I will assume `dt_strata` = `Date` formatted.
    
    out['dt_strata'] = dt_series.dt.strftime('%m/%d/%Y')
    
    # Calculate DOW
    # Mon=1, Tue=2, ..., Sat=6, Sun=0
    out['dow'] = (dt_series.dt.weekday + 1) % 7
    
    # Rename hourly columns
    for h in range(1, 25):
        out[f'pct_hourly_{h:02d}00'] = source[str(h)]
        
    # Add pct_hourly_2500 as null
    out['pct_hourly_2500'] = np.nan
    
    return out
