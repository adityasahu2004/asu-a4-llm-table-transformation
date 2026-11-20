import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format date as requested
    out = pd.DataFrame(index=source.index)
    out['date'] = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Define the mapping from source column names to target column names
    # Source: Hour 1 (1 AM) ... Hour 12 (12 PM) ... Hour 24 (12 AM/24:00)
    # Target order: 1AM, 2AM, ..., 11AM, 12AM, 1PM, ..., 11PM, 12PM
    
    # Helper to generate target names
    def get_target_name(h):
        if h == 12:
            return "12:00 PM"
        elif h == 24:
            return "12:00 AM"
        elif h < 12:
            return f"{h}:00 AM"
        else:
            return f"{h-12}:00 PM"

    # Construct the target columns in the specific order observed in the target schema sample
    # Order: 1-11 AM, 12 AM, 1-11 PM, 12 PM
    
    # 1-11 AM
    for h in range(1, 12):
        out[get_target_name(h)] = source[f'Hour {h}']
        
    # 12 AM (Source Hour 24)
    out[get_target_name(24)] = source['Hour 24']
    
    # 1-11 PM (Source Hours 13-23)
    for h in range(13, 24):
        out[get_target_name(h)] = source[f'Hour {h}']
        
    # 12 PM (Source Hour 12)
    out[get_target_name(12)] = source['Hour 12']
    
    return out.reset_index(drop=True)
