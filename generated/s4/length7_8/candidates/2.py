import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    
    # Format month name right-padded to 10 characters
    out['month'] = dates.dt.strftime('%B').str.ljust(10)
    
    # Determine day type: weekend if Saturday (5) or Sunday (6) in 0-indexed dayofweek
    out['daytype'] = dates.dt.dayofweek.apply(lambda x: 'weekend' if x >= 5 else 'weekday')
    
    # Rename hourly columns
    for h in range(1, 25):
        out[f'hr{h}'] = source[f'Hr {h}']
        
    return out.reset_index(drop=True)
