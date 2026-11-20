import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create the output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Derive month name
    out['month'] = dates.dt.strftime('%B')
    
    # Derive daytype: weekday (Mon-Fri) or weekend (Sat-Sun)
    # dayofweek: Monday=0, Sunday=6
    out['daytype'] = dates.dt.dayofweek.apply(lambda x: 'weekend' if x >= 5 else 'weekday')
    
    # Rename and map the hourly columns
    for h in range(1, 25):
        out[f'hr{h}'] = source[f'Hour {h}']
        
    return out.reset_index(drop=True)
