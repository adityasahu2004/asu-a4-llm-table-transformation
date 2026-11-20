import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'])
    
    # Create the output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Derive month and daytype
    out['month'] = dt.dt.strftime('%B')
    out['daytype'] = dt.apply(lambda x: 'weekday' if x.dayofweek < 5 else 'weekend')
    
    # Rename and copy hourly columns
    for h in range(1, 25):
        out[f'hr{h}'] = source[f'Hour {h}']
        
    return out.reset_index(drop=True)
