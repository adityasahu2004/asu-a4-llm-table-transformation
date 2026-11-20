import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format as MM/DD/YYYY
    dt = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Mapping from source column suffix (hour index) to target column name
    # Source hours are 1-24. 
    # 1-11 -> 1:00 AM - 11:00 AM
    # 12 -> 12:00 AM (Midnight) -- Wait, standard 12-hour clock:
    # 00:00 is 12:00 AM. 
    # 01:00 is 1:00 AM.
    # ...
    # 11:00 is 11:00 AM.
    # 12:00 is 12:00 PM (Noon).
    # 13:00 is 1:00 PM.
    # ...
    # 23:00 is 11:00 PM.
    # 24:00 is 12:00 AM (Midnight of next day, or end of day).
    
    # Let's look at the target sample order:
    # 1:00 AM, 2:00 AM, ..., 11:00 AM, 12:00 AM, 1:00 PM, ..., 11:00 PM, 12:00 PM
    
    # This order is unusual. Let's trace the values from the first sample row.
    # Source PCT_HOURLY_0100 = 0.0012220171 -> Target "1:00 AM" = 0.0012220171
    # Source PCT_HOURLY_1200 = 0.0012350173 -> Target "12:00 AM" = 0.0012350173 ??
    # Wait, let's look closer at the target sample data vs source sample data.
    
    # Source Row 1:
    # PCT_HOURLY_0100: 0.0012220171
    # PCT_HOURLY_1200: 0.0019548904
    # PCT_HOURLY_1300: 0.0019824444
    
    # Target Row 1:
    # "1:00 AM": 0.0012220171 (Matches Source 0100)
    # ...
    # "11:00 AM": 0.0011830166 (Matches Source 1100: 0.0011830166)
    # "12:00 AM": 0.0012350173 (Matches Source 1200? No, Source 1200 is 0.0019548904. 
    #                      Let's check Source 1200 in sample. 
    #                      Sample Source 1200 value is 0.0019548904.
    #                      Target "12:00 AM" value is 0.0012350173.
    #                      Which source column is 0.0012350173?
    #                      Looking at source: PCT_HOURLY_1200 is 0.0019548904.
    #                      PCT_HOURLY_0000 doesn't exist.
    #                      Let's check PCT_HOURLY_1200 in the source schema. It exists.
    #                      Let's check the value 0.0012350173 in the source row 1.
    #                      It is NOT in the first row of source data provided in the prompt?
    #                      Ah, the sample data in the prompt for Source and Target might not be row-aligned 1-to-1 in the JSON snippet display if they are just subsets.
    #                      However, the problem states "Infer the transformation". Usually, these are aligned.
    #                      Let's look at the Target Sample Row 1: "01/01/2016".
    #                      Source Sample Row 1: "7/2/2016".
    #                      They are NOT aligned by row index in the sample display. The sample display just shows *some* rows.
    #                      We must infer the mapping from column names and standard time conventions.
    
    # Standard mapping for 24-hour to 12-hour:
    # Hour 1 (01:00) -> 1:00 AM
    # Hour 2 (02:00) -> 2:00 AM
    # ...
    # Hour 11 (11:00) -> 11:00 AM
    # Hour 12 (12:00) -> 12:00 PM (Noon)
    # Hour 13 (13:00) -> 1:00 PM
    # ...
    # Hour 23 (23:00) -> 11:00 PM
    # Hour 24 (24:00) -> 12:00 AM (Midnight)
    
    # Let's verify this hypothesis against the Target Column Names order in the JSON:
    # Target Columns: 
    # 1:00 AM, 2:00 AM, ..., 11:00 AM, 
    # 12:00 AM, 
    # 1:00 PM, ..., 11:00 PM, 
    # 12:00 PM
    
    # This target column order is:
    # 1-11 AM
    # 12 AM (which corresponds to Hour 24 or Hour 0)
    # 1-11 PM
    # 12 PM (which corresponds to Hour 12)
    
    # Let's map Source Columns to Target Columns based on this logic:
    # PCT_HOURLY_0100 -> 1:00 AM
    # PCT_HOURLY_0200 -> 2:00 AM
    # ...
    # PCT_HOURLY_1100 -> 11:00 AM
    # PCT_HOURLY_2400 -> 12:00 AM  (Assuming 24:00 is midnight)
    # PCT_HOURLY_1300 -> 1:00 PM
    # ...
    # PCT_HOURLY_2300 -> 11:00 PM
    # PCT_HOURLY_1200 -> 12:00 PM
    
    # Let's double check if "12:00 AM" in target corresponds to Source 2400 or 0000.
    # Source has PCT_HOURLY_2400. It does not have 0000.
    # So PCT_HOURLY_2400 -> 12:00 AM.
    # PCT_HOURLY_1200 -> 12:00 PM.
    
    # The target columns are listed in a specific order in the JSON `columns` list.
    # We must preserve this order or simply rename and let pandas handle it? 
    # The instruction says "Keep target column names exactly". It doesn't explicitly enforce order, 
    # but usually it's good practice. The sample data shows the order.
    
    mapping = {
        'PCT_HOURLY_0100': '1:00 AM',
        'PCT_HOURLY_0200': '2:00 AM',
        'PCT_HOURLY_0300': '3:00 AM',
        'PCT_HOURLY_0400': '4:00 AM',
        'PCT_HOURLY_0500': '5:00 AM',
        'PCT_HOURLY_0600': '6:00 AM',
        'PCT_HOURLY_0700': '7:00 AM',
        'PCT_HOURLY_0800': '8:00 AM',
        'PCT_HOURLY_0900': '9:00 AM',
        'PCT_HOURLY_1000': '10:00 AM',
        'PCT_HOURLY_1100': '11:00 AM',
        'PCT_HOURLY_2400': '12:00 AM', # Midnight
        'PCT_HOURLY_1300': '1:00 PM',
        'PCT_HOURLY_1400': '2:00 PM',
        'PCT_HOURLY_1500': '3:00 PM',
        'PCT_HOURLY_1600': '4:00 PM',
        'PCT_HOURLY_1700': '5:00 PM',
        'PCT_HOURLY_1800': '6:00 PM',
        'PCT_HOURLY_1900': '7:00 PM',
        'PCT_HOURLY_2000': '8:00 PM',
        'PCT_HOURLY_2100': '9:00 PM',
        'PCT_HOURLY_2200': '10:00 PM',
        'PCT_HOURLY_2300': '11:00 PM',
        'PCT_HOURLY_1200': '12:00 PM'  # Noon
    }
    
    # Select and rename
    df = source[list(mapping.keys())]
    df = df.rename(columns=mapping)
    
    # Add date column at the beginning
    df.insert(0, 'date', out['date'])
    
    return df.reset_index(drop=True)
