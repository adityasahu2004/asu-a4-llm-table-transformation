import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Derive month and daytype
    out['month'] = dt.dt.strftime('%B')
    out['daytype'] = dt.dt.apply(lambda x: 'weekend' if x.dayofweek >= 5 else 'weekday')
    
    # Rename and copy hourly columns
    for h in range(1, 25):
        out[f'hr{h}'] = source[f'Hour {h}']
        
    return out.reset_index(drop=True)
