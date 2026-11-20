import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # The source format is M/D/YYYY (e.g., "7/3/2014")
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create dt_strata formatted as M/D/YYYY (no leading zeros for single digit months/days)
    # strftime %m and %d usually zero-pad, but the target sample shows "1/1/2014".
    # We can use .dt.strftime('%m/%d/%Y') and then strip leading zeros if necessary, 
    # or rely on the fact that pandas might handle it. However, standard strftime %m is 01.
    # Let's check the target sample: "1/1/2014". 
    # We will format as %m/%d/%Y and replace leading zeros for single digits if needed, 
    # or simply use a custom formatter. 
    # Actually, simplest way to get "1/1/2014" from datetime is often handled by specific formatting.
    # Let's use apply to strip leading zeros from month and day parts if they are single digits.
    dt_strata = dates.dt.strftime('%m/%d/%Y').apply(lambda x: 
        '/'.join([part.lstrip('0') if part.startswith('0') and len(part)==2 else part for part in x.split('/')])
    )
    
    # Calculate dow: Monday=0, Tuesday=1, ..., Sunday=6
    dow = dates.dt.dayofweek
    
    # Map source columns to target columns
    # Source Order: 1AM, 2AM, ..., 11AM, 12AM, 1PM, ..., 11PM, 12PM
    # Target Order: Hour 1 (1AM) ... Hour 11 (11AM), Hour 12 (12PM), Hour 13 (1PM) ... Hour 23 (11PM), Hour 24 (12AM)
    
    # Define the mapping from Target Hour Index to Source Column Name
    # Hour 1 -> 1:00 AM
    # Hour 2 -> 2:00 AM
    # ...
    # Hour 11 -> 11:00 AM
    # Hour 12 -> 12:00 PM  (Noon)
    # Hour 13 -> 1:00 PM
    # ...
    # Hour 23 -> 11:00 PM
    # Hour 24 -> 12:00 AM  (Midnight)
    
    source_col_map = {
        1: '1:00 AM',
        2: '2:00 AM',
        3: '3:00 AM',
        4: '4:00 AM',
        5: '5:00 AM',
        6: '6:00 AM',
        7: '7:00 AM',
        8: '8:00 AM',
        9: '9:00 AM',
        10: '10:00 AM',
        11: '11:00 AM',
        12: '12:00 PM',
        13: '1:00 PM',
        14: '2:00 PM',
        15: '3:00 PM',
        16: '4:00 PM',
        17: '5:00 PM',
        18: '6:00 PM',
        19: '7:00 PM',
        20: '8:00 PM',
        21: '9:00 PM',
        22: '10:00 PM',
        23: '11:00 PM',
        24: '12:00 AM'
    }
    
    result = pd.DataFrame()
    result['dt_strata'] = dt_strata
    result['dow'] = dow
    
    for h in range(1, 25):
        result[f'pct_hourly_{h:02d}00'] = source[source_col_map[h]]
        
    result['pct_hourly_2500'] = 0
    
    return result
