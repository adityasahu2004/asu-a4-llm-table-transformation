import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format the date as required
    date_str = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Map source columns to target Hour columns
    # Hour 1-11: 1:00 AM - 11:00 AM
    # Hour 12: 12:00 PM
    # Hour 13-23: 1:00 PM - 11:00 PM
    # Hour 24: 12:00 AM
    
    out = pd.DataFrame(index=source.index)
    out['date'] = date_str
    
    # 1:00 AM to 11:00 AM -> Hour 1 to Hour 11
    for h in range(1, 12):
        out[f'Hour {h}'] = source[f'{h}:00 AM']
        
    # 12:00 PM -> Hour 12
    out['Hour 12'] = source['12:00 PM']
    
    # 1:00 PM to 11:00 PM -> Hour 13 to Hour 23
    for h in range(1, 12):
        out[f'Hour {h + 12}'] = source[f'{h}:00 PM']
        
    # 12:00 AM -> Hour 24
    out['Hour 24'] = source['12:00 AM']
    
    return out.reset_index(drop=True)
