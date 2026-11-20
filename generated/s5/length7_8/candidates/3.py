import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Format month name: e.g., "January   " (10 chars)
    out['month'] = dates.dt.strftime('%B').str.ljust(10)
    
    # Determine daytype: weekday (Mon-Fri) or weekend (Sat-Sun)
    # dayofweek: Mon=0 ... Sun=6
    out['daytype'] = dates.dt.dayofweek.apply(lambda x: 'weekend' if x >= 5 else 'weekday')
    
    # Rename and project hourly columns
    for h in range(1, 25):
        out[f'hr{h}'] = source[f'Hr {h}']
        
    return out.reset_index(drop=True)
