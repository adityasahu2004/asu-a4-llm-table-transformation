import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Format date column
    out = pd.DataFrame(index=source.index)
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Define mapping from source hour (int) to target column name
    # Source 1-11 -> 1 AM - 11 AM
    # Source 12 -> 12 AM (Noon)
    # Source 13-23 -> 1 PM - 11 PM
    # Source 24 -> 12 PM (Midnight)
    
    for h in range(1, 12):
        out[f'{h}:00 AM'] = source[str(h)]
        
    out['12:00 AM'] = source['12']
    
    for h in range(13, 24):
        pm_h = h - 12
        out[f'{pm_h}:00 PM'] = source[str(h)]
        
    out['12:00 PM'] = source['24']
    
    # Select columns in the exact order specified by target schema
    cols = ['date']
    cols += [f'{h}:00 AM' for h in range(1, 12)]
    cols.append('12:00 AM')
    cols += [f'{h}:00 PM' for h in range(1, 12)]
    cols.append('12:00 PM')
    
    return out[cols].reset_index(drop=True)
