import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create the output DataFrame
    out = pd.DataFrame(index=source.index)
    
    # Format date as MM/DD/YYYY
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Rename hour columns from '1'...'24' to 'Hour 1'...'Hour 24'
    for h in range(1, 25):
        out[f'Hour {h}'] = source[h]
        
    return out.reset_index(drop=True)
