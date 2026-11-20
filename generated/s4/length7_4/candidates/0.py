import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Derive month: Full name, padded to 10 chars
    # e.g., January (7) + 3 spaces = 10
    # February (8) + 2 spaces = 10
    # March (5) + 5 spaces = 10
    out['month'] = dt.dt.strftime('%B').str.ljust(10)
    
    # Derive daytype
    # weekday() returns 0-4 for Mon-Fri, 5-6 for Sat-Sun
    out['daytype'] = dt.dt.weekday().apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # Rename value columns to hr columns
    for i in range(1, 25):
        out[f'hr{i}'] = source[f'value{i}']
        
    return out.reset_index(drop=True)
