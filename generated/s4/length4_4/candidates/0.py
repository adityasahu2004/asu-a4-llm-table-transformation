import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    out['date'] = dates.dt.strftime('%m/%d/%Y')
    
    # Define the mapping from source column names (strings "1"-"24") to target names
    # Source columns are named "1", "2", ..., "24"
    # Target order is specific:
    # 1-11 AM
    # 12 AM (Midnight, source 24? No, usually 12 AM is midnight. Let's check standard mapping.
    # Usually: 
    # 1 AM = Source 1
    # ...
    # 11 AM = Source 11
    # 12 PM = Source 12 (Noon)
    # 1 PM = Source 13
    # ...
    # 11 PM = Source 23
    # 12 AM = Source 24 (Midnight)
    #
    # However, the target column list is:
    # 1:00 AM ... 11:00 AM, 12:00 AM, 1:00 PM ... 11:00 PM, 12:00 PM
    #
    # Let's look at the data to verify if 12:00 AM corresponds to source 24 or 12.
    # In standard 24h to 12h conversion:
    # 00:00 (24) -> 12:00 AM
    # 12:00 (12) -> 12:00 PM
    #
    # The target schema has "12:00 AM" at index 11 (0-indexed) in the column list, 
    # and "12:00 PM" at index 23 (last).
    #
    # Let's assume standard mapping:
    # Source 1 -> 1:00 AM
    # Source 2 -> 2:00 AM
    # ...
    # Source 11 -> 11:00 AM
    # Source 24 -> 12:00 AM  (Midnight)
    # Source 13 -> 1:00 PM
    # Source 14 -> 2:00 PM
    # ...
    # Source 23 -> 11:00 PM
    # Source 12 -> 12:00 PM  (Noon)
    
    # Construct the list of (target_name, source_name) pairs in the exact target order
    mapping = [
        ("1:00 AM", "1"),
        ("2:00 AM", "2"),
        ("3:00 AM", "3"),
        ("4:00 AM", "4"),
        ("5:00 AM", "5"),
        ("6:00 AM", "6"),
        ("7:00 AM", "7"),
        ("8:00 AM", "8"),
        ("9:00 AM", "9"),
        ("10:00 AM", "10"),
        ("11:00 AM", "11"),
        ("12:00 AM", "24"),  # Midnight
        ("1:00 PM", "13"),
        ("2:00 PM", "14"),
        ("3:00 PM", "15"),
        ("4:00 PM", "16"),
        ("5:00 PM", "17"),
        ("6:00 PM", "18"),
        ("7:00 PM", "19"),
        ("8:00 PM", "20"),
        ("9:00 PM", "21"),
        ("10:00 PM", "22"),
        ("11:00 PM", "23"),
        ("12:00 PM", "12")   # Noon
    ]
    
    for target_col, source_col in mapping:
        out[target_col] = source[source_col]
        
    return out.reset_index(drop=True)
